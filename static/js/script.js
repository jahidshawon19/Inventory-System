const API_URL = "http://127.0.0.1:8000/api/products/";

function loadProducts() {
    fetch(API_URL)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("productList");
            list.innerHTML = "";
            data.forEach(p => {
                list.innerHTML += `
                    <li>
                        ${p.name} - ${p.quantity} x ${p.unit_price} = ${p.total_price}
                        <button onclick="deleteProduct(${p.id})">Delete</button>
                    </li>
                `;
            });
        });
}

function addProduct() {
    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            unit_price: document.getElementById("unit_price").value,
            quantity: document.getElementById("quantity").value
        })
    }).then(() => loadProducts());
}

function deleteProduct(id) {
    fetch(API_URL + id + "/", {
        method: "DELETE"
    }).then(() => loadProducts());
}

loadProducts();
