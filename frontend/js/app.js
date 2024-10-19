function loadCupcakes() {
    fetch('/cupcakes')
    .then(response => response.json())
    .then(data => {
        let cupcakeList = document.getElementById('cupcake-list');
        cupcakeList.innerHTML = '';
        data.forEach(cupcake => {
            let item = document.createElement('div');
            item.innerHTML = `<h3>${cupcake.name}</h3><p>${cupcake.description}</p>`;
            cupcakeList.appendChild(item);
        });
    });
}
