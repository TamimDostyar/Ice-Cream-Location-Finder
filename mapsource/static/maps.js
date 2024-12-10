document.addEventListener("DOMContentLoaded", function () {
    var streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    var satelliteLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data: &copy; <a href="https://www.opentopomap.org/">OpenTopoMap</a> contributors'
    });

    var terrainLayer = L.tileLayer('https://{s}.tile.stamen.com/terrain/{z}/{x}/{y}.jpg', {
        attribution: '&copy; <a href="https://www.stamen.com/">Stamen Design</a>'
    });
    var map = L.map('map', {
        center: [51.505, -0.09],
        zoom: 13,
        layers: [streetLayer]
    });
    var baseMaps = {
        "Street Map": streetLayer,
        "Satellite Map": satelliteLayer,
        "Terrain Map": terrainLayer
    };

    L.control.layers(baseMaps).addTo(map);

    L.marker([51.5, -0.09]).addTo(map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup();

    var routeControl;

    function findLocation() {
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by your browser');
            return;
        }

        function success(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            map.setView([lat, lon], 13);
            L.marker([lat, lon]).addTo(map)
                .bindPopup('You are here!')
                .openPopup();

            const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;

            axios.get(url)
                .then(response => {
                    const location = response.data.address;
                    const city = location.city || location.town || location.village || 'Unknown City';
                    const state = location.state || 'Unknown State';
                    const country = location.country || 'Unknown Country';
                    document.getElementById('location-info').innerText = `${city}, ${state}, ${country}`;
                    document.getElementById('location-info').style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching the location:', error);
                });
        }

        function error() {
            alert('Unable to retrieve your location');
        }

        navigator.geolocation.getCurrentPosition(success, error);
    }
    function findShops() {
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by your browser');
            return;
        }

        function success(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=ice_cream](around:5000,${lat},${lon});out;`;

            axios.get(overpassUrl)
                .then(response => {
                    const shops = response.data.elements;
                    const shopList = document.getElementById('shop-list');
                    shopList.innerHTML = '<h3 class="title is-4">Ice Cream Shops Nearby:</h3>';
                    if (shops.length === 0) {
                        shopList.innerHTML += '<p>No ice cream shops found nearby.</p>';
                    } else {
                        shopList.innerHTML += '<ul>';
                        shops.forEach(shop => {
                            const shopName = shop.tags.name || 'Unnamed Ice Cream Shop';
                            shopList.innerHTML += `<li>${shopName}</li>`;
                            const shopLat = shop.lat;
                            const shopLon = shop.lon;
                            L.marker([shopLat, shopLon]).addTo(map)
                                .bindPopup(shopName);
                        });
                        shopList.innerHTML += '</ul>';
                    }
                    shopList.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error fetching ice cream shops:', error);
                });
        }

        function error() {
            alert('Unable to retrieve your location');
        }

        navigator.geolocation.getCurrentPosition(success, error);
    }
    document.getElementById('find-me').addEventListener('click', findLocation);
    document.getElementById('find-shops').addEventListener('click', findShops);

    var userLat, userLon;

    navigator.geolocation.getCurrentPosition(function (position) {
        userLat = position.coords.latitude;
        userLon = position.coords.longitude;
    });

    function setDestination(lat, lon, placeName, displayName) {
        if (routeControl) {
            map.removeControl(routeControl);
        }
        routeControl = L.Routing.control({
            waypoints: [
                L.latLng(userLat, userLon),
                L.latLng(lat, lon)
            ],
            routeWhileDragging: true,
            geocoder: L.Control.Geocoder.nominatim(),
            createMarker: function (i, wp, nWps) {
                return L.marker(wp.latLng, {
                    draggable: true,
                    icon: L.icon.glyph({ glyph: i === 0 ? '🚩' : '🏁' })
                }).bindPopup(i === 0 ? 'Start' : 'Destination');
            }
        }).addTo(map);
        var distance = map.distance([userLat, userLon], [lat, lon]);
        document.getElementById('location-info').innerHTML = `Place: ${placeName}<br>Address: ${displayName}<br>Distance: ${(distance / 1000).toFixed(2)} km`;
        document.getElementById('location-info').style.display = 'block';
    }
    map.on('click', function (e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;

        axios.get(url)
            .then(response => {
                const location = response.data.address;
                const placeName = location.amenity || location.building || location.shop || location.tourism || 'Unknown Place';
                const displayName = response.data.display_name;

                var popupContent = `Place: ${placeName}<br>Address: ${displayName}<br><button id="set-destination">Set as Destination</button>`;
                var popup = L.popup()
                    .setLatLng(e.latlng)
                    .setContent(popupContent)
                    .openOn(map);
                document.getElementById('set-destination').addEventListener('click', function () {
                    setDestination(lat, lon, placeName, displayName);
                });
            })
            .catch(error => {
                console.error('Error fetching the place details:', error);
            });
    });
});
