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
        const { title } = item;
        console.log(item)
        return `<div>${title}</div>`;
    }).join('');
};


function iceCreamSelector(url) {
    let myiceCreamSelector = document.querySelector(".iceCreamType")


}