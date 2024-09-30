document.getElementById('searchBar').addEventListener('keyup', (e) => {
    const searchData = e.target.value.toLowerCase();
    const filterData = categories.filter((item) => {
        return (
            item.title.toLowerCase().includes(searchData)
        );
    });
    displayItem(filterData);
});

const displayItem = (items) => {
    document.getElementById('root').innerHTML = items.map((item) => {
        const { title } = item; // Destructure title from item
        console.log(item)
        return `<div>${title}</div>`; // Return the HTML for each item
    }).join(''); // Join the array of HTML strings into one string
};
