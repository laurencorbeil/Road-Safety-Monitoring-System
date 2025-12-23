let map = L.map('map').setView([43.136389, -79.1075], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let markers = [];
let currentPolyline = null;

map.on('click', function(e) {
    if (markers.length === 2) {
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        // remove previous route when starting a new selection
        if (currentPolyline) {
            map.removeLayer(currentPolyline);
            currentPolyline = null;
        }
    }

    markers.push(L.marker(e.latlng).addTo(map));
});

function go() {
    if (markers.length < 2) {
        alert('Please select two points on the map first.');
        return;
    }

    //get start and end points
    let start = [markers[0].getLatLng().lat, markers[0].getLatLng().lng];
    let end   = [markers[1].getLatLng().lat, markers[1].getLatLng().lng];
    
    // get selected algo from the UI if available
    const algo = (window.getSelectedAlgorithm && typeof window.getSelectedAlgorithm === 'function') ? getSelectedAlgorithm() : 'astar';

    fetch("/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start, end, algo })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert('Routing error: ' + data.error);
            return;
        }

        // remove old line
        if (currentPolyline) {
            map.removeLayer(currentPolyline);
            currentPolyline = null;
        }

        // draw line
        currentPolyline = L.polyline(data.path, {color: 'blue'}).addTo(map);
        try {
            const hull = computeConvexHull(data.path);
            if (hull && hull.length >= 3) {
                if (currentPolygon) { map.removeLayer(currentPolygon); }
                currentPolygon = L.polygon(hull, {color: 'orange', weight: 2, fillOpacity: 0.05}).addTo(map);
            }
        } catch(e) {
            console.warn('Could not draw hull:', e);
        }

        try { map.fitBounds(currentPolyline.getBounds(), {padding: [20,20]}); } catch(e){}

        const distance = data.distance_m != null ? (data.distance_m >= 1000 ? (data.distance_m/1000).toFixed(2) + ' km' : Math.round(data.distance_m) + ' m') : null;
        const nodes = data.node_path ? data.node_path.length : null;
        const details = { time: data.time_s != null ? Number(data.time_s).toFixed(4) + ' s' : null, text: nodes ? data.node_path.join(' → ') : null };

        if (window.updateInfo && typeof window.updateInfo === 'function') {
            updateInfo(distance, nodes, details);
        }
    })
    .catch(err => {
        alert('Network error: ' + err.message);
    });
}

// draw the box around the selected area 
const permanentBorder = [
    [43.1413888889, -79.1011111111],
    [43.1430555556, -79.1127777778],
    [43.13,          -79.1125],
    [43.13,          -79.1]
];

const perm = L.polygon(permanentBorder, {weight: 3, dashArray: '6 6', fillOpacity: 0.04}).addTo(map);