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

    // Add marker
    L.marker([51.5, -0.09]).addTo(map)
        .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
        .openPopup();

    var currentCity = '';

    function updateLocationInfo(city, state, country) {
        currentCity = city;
        document.getElementById('location-info').innerText = `${city}, ${state}, ${country}`;
        document.getElementById('location-info').style.display = 'block';
    }

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
                    updateLocationInfo(city, state, country);
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

    function searchCity() {
        const query = document.getElementById('search-input').value;
        const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(query)}`;

        axios.get(url)
            .then(response => {
                if (response.data.length > 0) {
                    const location = response.data[0];
                    const lat = location.lat;
                    const lon = location.lon;
                    map.setView([lat, lon], 13);
                    L.marker([lat, lon]).addTo(map)
                        .bindPopup(`Location: ${location.display_name}`)
                        .openPopup();

                    const city = location.address.city || location.address.town || location.address.village || 'Unknown City';
                    const state = location.address.state || 'Unknown State';
                    const country = location.address.country || 'Unknown Country';
                    updateLocationInfo(city, state, country);
                } else {
                    alert('Location not found');
                }
            })
            .catch(error => {
                console.error('Error searching for the location:', error);
            });
    }

    function fetchIceCreamShops(city) {
        const API_KEY = "ZYCLMu7E4I28mgvHbILO4nJyehGiEu63YpxN1ig3ftP4P3P8V3b7Rw7xr38gd_gfNGI6CHtCl59wVfmLVNF0oht5HMK9G2gGhTYCNFi1hUUhxBxj1GZhJ25XK5NYZ3Yx";
        const YELP_API_URL = "https://api.yelp.com/v3/businesses/search";

        axios.get(YELP_API_URL, {
            headers: {
                Authorization: `Bearer ${API_KEY}`
            },
            params: {
                location: city,
                term: "ice cream",
                radius: 20000,
                sort_by: "best_match",
                limit: 20
            }
        })
            .then(response => {
                const shops = response.data.businesses;
                const shopList = document.getElementById('shop-list');
                shopList.innerHTML = '<h3 class="title is-4">Ice Cream Shops Nearby:</h3>';
                if (shops.length === 0) {
                    shopList.innerHTML += '<p>No ice cream shops found nearby.</p>';
                } else {
                    const columns = document.createElement("div");
                    columns.className = "columns is-multiline";

                    shops.forEach(shop => {
                        const column = document.createElement("div");
                        column.className = "column is-one-third";

                        const card = document.createElement("div");
                        card.className = "card";

                        const cardImage = document.createElement("div");
                        cardImage.className = "card-image";
                        const figure = document.createElement("figure");
                        figure.className = "image is-4by3";
                        const img = document.createElement("img");
                        img.src = shop.image_url || 'https://media.istockphoto.com/id/957740086/photo/boy-share-ice-cream-with-his-sister.jpg?s=612x612&w=0&k=20&c=4j5yubH5Ggv0Cfwk7gYrFOYb0XMFTBww477JIaRn5_s=';
                        img.alt = shop.name;
                        img.classList.add("is-rounded");

                        figure.appendChild(img);
                        cardImage.appendChild(figure);
                        card.appendChild(cardImage);

                        const cardContent = document.createElement("div");
                        cardContent.className = "card-content";
                        const title = document.createElement("p");
                        title.className = "title is-4";
                        title.innerText = shop.name;
                        const address = document.createElement("p");
                        address.innerText = shop.location.display_address.join(', ');
                        const rating = document.createElement("p");
                        rating.innerText = `Rating: ${shop.rating} stars`;

                        cardContent.appendChild(title);
                        cardContent.appendChild(address);
                        cardContent.appendChild(rating);
                        card.appendChild(cardContent);

                        column.appendChild(card);
                        columns.appendChild(column);

                        L.marker([shop.coordinates.latitude, shop.coordinates.longitude]).addTo(map)
                            .bindPopup(`${shop.name}<br>${shop.location.display_address.join(', ')}`);
                    });

                    shopList.appendChild(columns);
                }
                shopList.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching ice cream shops:', error);
            });
    }

    document.getElementById('find-me').addEventListener('click', findLocation);
    document.getElementById('find-shops').addEventListener('click', function () {
        fetchIceCreamShops(currentCity);
    });
    document.getElementById('search-btn').addEventListener('click', searchCity);
});
