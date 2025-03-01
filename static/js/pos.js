// Medical Shop POS System - POS Module
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart
    let cart = [];
    let totalAmount = 0;
    
    // DOM Elements
    const medicineCards = document.querySelectorAll('.medicine-card');
    const cartItemsContainer = document.getElementById('cart-items');
    const totalDisplay = document.getElementById('total-amount');
    const checkoutBtn = document.getElementById('checkout-btn');
    const paymentMethodSelect = document.getElementById('payment-method');
    const categoryFilters = document.querySelectorAll('.category-filter');
    const searchInput = document.getElementById('search-medicine');
    
    // Add event listeners to medicine cards
    medicineCards.forEach(card => {
        card.addEventListener('click', function() {
            const medicineId = this.getAttribute('data-id');
            getMedicineDetails(medicineId);
        });
    });
    
    // Filter medicines by category
    if (categoryFilters) {
        categoryFilters.forEach(filter => {
            filter.addEventListener('click', function(e) {
                e.preventDefault();
                const categoryId = this.getAttribute('data-category');
                
                // Highlight active category
                categoryFilters.forEach(f => f.classList.remove('active'));
                this.classList.add('active');
                
                // Show/hide medicine cards
                medicineCards.forEach(card => {
                    if (categoryId === 'all' || card.getAttribute('data-category') === categoryId) {
                        card.parentElement.style.display = 'block';
                    } else {
                        card.parentElement.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // Search medicines
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            medicineCards.forEach(card => {
                const medicineName = card.querySelector('.card-title').textContent.toLowerCase();
                if (medicineName.includes(searchTerm)) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    }
    
    // Get medicine details from API
    function getMedicineDetails(medicineId) {
        fetch(`/api/medicine/${medicineId}/`)
            .then(response => response.json())
            .then(data => {
                // Check if already in cart
                const existingItem = cart.find(item => item.id === data.id);
                
                if (existingItem) {
                    // Check stock availability
                    if (existingItem.quantity < data.available) {
                        existingItem.quantity += 1;
                        updateCart();
                    } else {
                        showAlert('No more stock available for this medicine', 'warning');
                    }
                } else {
                    // Check stock availability
                    if (data.available > 0) {
                        // Add to cart
                        cart.push({
                            id: data.id,
                            name: data.name,
                            price: data.price,
                            quantity: 1,
                            available: data.available
                        });
                        updateCart();
                    } else {
                        showAlert('This medicine is out of stock', 'warning');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Failed to get medicine details', 'danger');
            });
    }
    
    // Update cart display
    function updateCart() {
        cartItemsContainer.innerHTML = '';
        totalAmount = 0;
        
        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            totalAmount += itemTotal;
            
            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item py-2';
            cartItemElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">₹${item.price.toFixed(2)} x ${item.quantity}</small>
                    </div>
                    <div>
                        <span class="h6 mb-0 me-2">₹${itemTotal.toFixed(2)}</span>
                        <div class="btn-group btn-group-sm" role="group">
                            <button type="button" class="btn btn-outline-secondary decrease-btn" data-index="${index}">-</button>
                            <button type="button" class="btn btn-outline-secondary increase-btn" data-index="${index}">+</button>
                            <button type="button" class="btn btn-outline-danger remove-btn" data-index="${index}">×</button>
                        </div>
                    </div>
                </div>
            `;
            
            cartItemsContainer.appendChild(cartItemElement);
        });
        
        // Update total display
        totalDisplay.textContent = totalAmount.toFixed(2);
        
        // Add event listeners to cart buttons
        document.querySelectorAll('.decrease-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                decreaseQuantity(index);
            });
        });
        
        document.querySelectorAll('.increase-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                increaseQuantity(index);
            });
        });
        
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                removeFromCart(index);
            });
        });
    }
    
    // Decrease item quantity
    function decreaseQuantity(index) {
        if (cart[index].quantity > 1) {
            cart[index].quantity -= 1;
        } else {
            removeFromCart(index);
        }
        updateCart();
    }
    
    // Increase item quantity
    function increaseQuantity(index) {
        if (cart[index].quantity < cart[index].available) {
            cart[index].quantity += 1;
            updateCart();
        } else {
            showAlert('No more stock available for this medicine', 'warning');
        }
    }
    
    // Remove item from cart
    function removeFromCart(index) {
        cart.splice(index, 1);
        updateCart();
    }
    
    // Checkout process
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            if (cart.length === 0) {
                showAlert('Cart is empty!', 'warning');
                return;
            }
            
            const paymentMethod = paymentMethodSelect.value;
            
            // Create sale object
            const saleData = {
                items: cart.map(item => ({
                    id: item.id,
                    quantity: item.quantity,
                    price: item.price
                })),
                total: totalAmount,
                payment_method: paymentMethod
            };
            
            // Send to API
            fetch('/api/sale/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(saleData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Sale completed successfully!', 'success');
                    cart = [];
                    updateCart();
                    setTimeout(() => {
                        window.location.href = `/sales/${data.sale_id}/`;
                    }, 1500);
                } else {
                    showAlert(data.error || 'Failed to complete sale', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Failed to complete sale', 'danger');
            });
        });
    }
    
    // Helper function to show alerts
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto dismiss after 3 seconds
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => {
                alertContainer.removeChild(alert);
            }, 150);
        }, 3000);
    }
    
    // Get CSRF token from cookies
    function getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        // If cookie method failed, try to get from the DOM (Django inserts it in forms)
        if (!cookieValue) {
            const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            if (csrfInput) {
                cookieValue = csrfInput.value;
            }
        }
        return cookieValue;
    }
});