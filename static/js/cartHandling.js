document.addEventListener('DOMContentLoaded', function() {
    addToCartButton = document.getElementById('add-to-cart');
    cartBtn = document.getElementById('add-to-cart-button');
    removeFromCartButton = document.getElementById('remove-from-cart');
    quantitySelector = document.getElementById('quantity-selector');
    removeBtn = document.getElementById('remove-btn');
    goToCartBtn = document.getElementById('go-to-cart-btn');
    decreaseBtn = document.getElementById('decrease-btn');
    quantity = document.getElementById('quantity');
    const productId = "{{ product.uid }}"; // Get the product ID from the template context
    const customerId = "{{ user.extra.uid }}"; // Get the product ID from the template context


    cartBtn.addEventListener('click', function(event) {
        event.preventDefault(); 
        console.log("Add to cart button clicked");
    
        const url = `{% url "addToCartAPI" user.extra.uid product.uid %}`; // Construct the URL
        fetch(url,{
            method: 'GET',
            headers:{
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('data.success:', data.success); // Handle the response data as needed
            if (data.success === true) {
                cartBtn.classList.add('hidden'); 
                cartBtn.classList.add('hidden');
                goToCartBtn.classList.remove('hidden');
                removeBtn.classList.remove('hidden'); 
                quantitySelector.classList.remove('hidden'); 
                quantity.value = data.quantity 
            } else {
                alert('Error adding to cart: ' + data.message);
            }
        });
    });

    addToCartButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default action
        console.log('adding to cart')
        const url = `{% url "addToCartAPI" user.extra.uid product.uid %}`; // Construct the URL
        fetch(url,{
            method: 'GET',
            headers:{
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('added to cart'); // Handle the response data as needed
            if (data.success === true) {
                cartBtn.classList.add('hidden'); // Hide the add to cart button
                goToCartBtn.classList.remove('hidden'); // Show the go to cart button
                removeBtn.classList.remove('hidden'); // Show the remove button
                quantitySelector.classList.remove('hidden'); // Show the quantity selector
                quantity.value = data.quantity // Update the quantity in the input field
                cartBtn.classList.add('hidden'); // Hide the add to cart button
            } else {
                alert('Error adding to cart: ' + data.message);
            }
        })
    });

    removeFromCartButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default action
        const productId = "{{ product.uid }}"; // Get the product ID from the template context
        const customerId = "{{ user.extra.uid }}"; // Get the product ID from the template context
        const url = `{% url "removeFromCartAPI" user.extra.uid product.uid %}`; // Construct the URL
        fetch(url,{
            method: 'GET',
            headers:{
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.success); // Handle the response data as needed
            if (data.success === true) {
                quantity.value = data.quantity // Update the quantity in the input field
                if(data.quantity == 0){
                    cartBtn.classList.remove('hidden'); // Show the add to cart button
                    goToCartBtn.classList.add('hidden'); // Hide the go to cart button
                    removeBtn.classList.add('hidden'); // Hide the remove button
                    quantitySelector.classList.add('hidden'); // Hide the quantity selector
                    decreaseBtn.disabled = true; // Disable the decrease button
                }
            } else {
                alert('Error adding to cart: ' + data.message);
            }
        })
    });
    

    });