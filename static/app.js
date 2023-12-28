function updateTime() {
    const timeContainer = document.getElementById('time');
    const userTime = new Date().toLocaleString(); // Get the current time in the user's time zone
    timeContainer.innerHTML = `Current time: ${userTime}`;
}

updateTime();

// Update the time every second
setInterval(updateTime, 1000);


// Get a reference to  to the h1 element
var welcomeMessage = document.getElementById("welcome-message");

// Get the content
var fullWelcomeMessage = welcomeMessage.textContent;

// Clear the content
welcomeMessage.textContent = "";

// Split the full message into an array of characters
var messageCharacters = fullWelcomeMessage.split("");

// Function to animate the entire message
function animateWelcomeMessage() {
  if (messageCharacters.length > 0) {
    welcomeMessage.textContent += messageCharacters.shift();
    setTimeout(animateWelcomeMessage, 150);
  }
}

animateWelcomeMessage();

function jumpToTop() {
  document.body.scroll = 0; // For Safari
  document.documentElement.scrollTop = 0 // For Chrome, FireFox, IE and Opera
}


// Sample product data with image URLs, names, and prices
const products = [
  { name: "Carbanent Sauvignon", price: 30, image: "/static/images/wine.jpg" },
  { name: "The Pyschology of Money", price: 15, image: "/static/images/book.jpg" },
  { name: "6 by 6 bed", price: 799, image: "/static/images/bed.jpg" },
  { name: "Bicycle(adults)", price: 211, image: "/static/images/bicycle.jpg"},
  { name: "iPhone 15(128GB)", price: 960, image: "/static/images/iphone.jpg"},
  { name: "HP laptop i7, 256SSD", price: 781, image: "/static/images/laptop.jpg"},
  { name: "Nike", price: 75, image: "/static/images/nike.jpg" },
  { name: "vans(Burgundy)", price: 35, image: "/static/images/vans.jpg" },
  { name: "airforce", price: 83, image: "/static/images/airforce.jpg" },
  { name: "Bicycle(adults)", price: 211, image: "/static/images/bicycle.jpg"},
  { name: "iPhone 15(128GB)", price: 960, image: "/static/images/iphone.jpg"},
  { name: "HP laptop i7, 256SSD", price: 781, image: "/static/images/laptop.jpg"},
  { name: "Carbanent Sauvignon", price: 30, image: "/static/images/wine.jpg" },
  { name: "The Pyschology of Money", price: 15, image: "/static/images/book.jpg" },
  { name: "6 by 6 bed", price: 799, image: "/static/images/bed.jpg" },
  { name: "Bicycle(adults)", price: 211, image: "/static/images/bicycle.jpg"},
  { name: "iPhone 15(128GB)", price: 960, image: "/static/images/iphone.jpg"},
  { name: "HP laptop i7, 256SSD", price: 781, image: "/static/images/laptop.jpg"},
  { name: "Nike", price: 75, image: "/static/images/nike.jpg" },
  { name: "vans(Burgundy)", price: 35, image: "/static/images/vans.jpg" },
  { name: "airforce", price: 83, image: "/static/images/airforce.jpg" },
  { name: "Bicycle(adults)", price: 211, image: "/static/images/bicycle.jpg"},
  { name: "iPhone 15(128GB)", price: 960, image: "/static/images/iphone.jpg"},
  { name: "HP laptop i7, 256SSD", price: 781, image: "/static/images/laptop.jpg"},
  { name: "Carbanent Sauvignon", price: 30, image: "/static/images/wine.jpg" },
  // Add more products with their respective name, price, and image
];

// Define a cart to store added items
let cart = [];

// Function to create product elements dynamically
function createProductElement(product) {
  const productDiv = document.createElement('div');
  productDiv.classList.add('product');

  const img = document.createElement('img');
    img.src = product.image;
    img.alt = product.name;
    productDiv.appendChild(img);

  const pName = document.createElement('p');
    pName.textContent = product.name;
    productDiv.appendChild(pName);

  const pPrice = document.createElement('p');
    pPrice.textContent = `$${product.price}`;
    productDiv.appendChild(pPrice);

  const quantityInput = document.createElement('input');
    quantityInput.type = 'number';
    quantityInput.value = 1; // Default quantity is 1
    quantityInput.setAttribute('data-product', product.name); // Add data attribute to identify the product
    quantityInput.min = 1; // Set minimum quantity value to 1
    quantityInput.name = "quantity" // This name attribute is for all browsers to access quantity addition
    productDiv.appendChild(quantityInput);

    // CSS styles for the input element
    quantityInput.style.padding = "5px";
    // quantityInput.style.width = "80px";
    // quantityInput.style.marginRight = "9px";
    // quantityInput.style.marginBottom = "9px";

    // Class for styling the decrement and increment buttons
    quantityInput.classList.add("styled-number-input")

  const button = document.createElement('button');
    button.textContent = 'Add to Cart';
    button.addEventListener('click', () => addToCart(product.name, product.price));
    productDiv.appendChild(button);

    // CSS styles for add to cart button
    button.style.marginTop = "6px";
    button.style.padding = "5px";
    button.style.cursor = "pointer";

  return productDiv;
}

// Function to add products dynamically to the container
function addProductsToContainer() {
  const productsContainer = document.getElementById('products-container');
  products.forEach(product => {
      const productElement = createProductElement(product);
      productsContainer.appendChild(productElement);
  });
}

// Function to add items with specified quantity to the cart
function addToCart(productName, price) {
  console.log("Adding ${productName} to the cart with price $${price");
  const quantityInput = document.querySelector(`input[type='number'][data-product="${productName}"]`);
  const quantity = parseInt(quantityInput.value);

  let existingItem = cart.find(item => item.name === productName);

  if (existingItem) {
      existingItem.quantity = quantity; // Set the quantity to the entered value
  } else {
      cart.push({ name: productName, price: price, quantity: quantity });
  }

  updateCart();
}


// Function to update the cart view and total prices based on quantity
function updateCart() {
  const cartItems = document.getElementById('cart-items');
  const cartTotal = document.getElementById('cart-total');

  cartItems.innerHTML = '';
  let total = 0;

  cart.forEach(item => {
      const itemTotal = item.price * item.quantity;
      total += itemTotal;

      const li = document.createElement('li');
      li.textContent = `${item.name} - Quantity: ${item.quantity} - $${itemTotal}`;
      cartItems.appendChild(li);
  });

  cartTotal.textContent = total;

  updateCartQuantityIcon();
}

const checkoutButton = document.getElementById("checkout-btn");
const clearCartButton = document.getElementById("clear-cart-btn");

checkoutButton.addEventListener("click", checkout);
clearCartButton.addEventListener("click", clearCart);

function checkout() {
  alert("Checked out completed! Thank you for shopping.");
  clearCart();
}

function toggleCartDropdown() {
  const cartDropdownContent = document.getElementById("cart-dropdown-content");
  cartDropdownContent.classList.toggle("show");

  updateCartQuantityIcon();
}

function updateCartQuantityIcon() {
  const cartQuantityIcon = document.getElementById("cart-quantity");
  // const cartIconQuantity = document.getElementById("cart-icon-quantity");
  const totalQuantity = cart.reduce((acc, item) => acc + item.quantity, 0);
  cartQuantityIcon.textContent = totalQuantity;
  // cartIconQuantity.textContent = totalQuantity;
}

// Function to clear the cart
function clearCart() {
  cart = [];
  updateCart();
}

// Invoke the function to add products to the container
addProductsToContainer();

// Find the cart icon element
const cartIconContainer = document.getElementById("cart-dropdown");
cartIconContainer.addEventListener("click", toggleCartDropdown);
