// JavaScript for the landing page will go here. 

// IMPORTANT: In a real application, this data would be fetched from a backend API.
// The backend API would read from a database or a file like fabric_data.py (which now contains logic to generate >100 items).
// For this prototype, we are hardcoding a large representative sample here to simulate the data availability.
const mockInventoryData = [
    // Initial 12 items from before for consistency
    { skuCode: "100084-000012-2", productName: "3-Shelf Bookcase / Grey / Small", location: "Warehouse East", channel: "Online Store", status: "Low stock", availToPurchase: 130, availToBackorder: 18, availToPreorder: 15 },
    { skuCode: "150085-000019-9", productName: "Oceanside Sideboard / Oak / Large", location: "Warehouse West", channel: "Retail Outlet A", status: "Low stock", availToPurchase: 540, availToBackorder: 56, availToPreorder: 54 },
    { skuCode: "540083-000017-7", productName: "Stairway Ladder Shelf / Brown / Tall", location: "Showroom Central", channel: "Online Store", status: "Available", availToPurchase: 536, availToBackorder: 82, availToPreorder: 13 },
    { skuCode: "760083-000015-2", productName: "Minimalist Coffee Table / Oak / Small", location: "Warehouse East", channel: "Retail Outlet B", status: "Backorder", availToPurchase: 274, availToBackorder: 15, availToPreorder: 12 },
    { skuCode: "420081-000015-2", productName: "Oceanside Sectional Sofa / White Linen", location: "Warehouse West", channel: "Online Store", status: "Preorder", availToPurchase: 0, availToBackorder: 0, availToPreorder: 135 },
    { skuCode: "B001-CHAIR-RED", productName: "Ergonomic Office Chair / Red Mesh", location: "Showroom Central", channel: "Retail Outlet A", status: "Available", availToPurchase: 75, availToBackorder: 5, availToPreorder: 0 },
    { skuCode: "D003-DESK-BLK", productName: "Standing Desk Converter / Black", location: "Warehouse East", channel: "Online Store", status: "Available", availToPurchase: 210, availToBackorder: 20, availToPreorder: 5 },
    { skuCode: "L005-LAMP-BRS", productName: "Industrial Floor Lamp / Brass Finish", location: "Warehouse West", channel: "Retail Outlet B", status: "Low stock", availToPurchase: 45, availToBackorder: 10, availToPreorder: 0 },
    { skuCode: "S007-SOFA-GRN", productName: "Velvet Loveseat / Emerald Green", location: "Showroom Central", channel: "Online Store", status: "Backorder", availToPurchase: 30, availToBackorder: 50, availToPreorder: 25 },
    { skuCode: "T009-TABLE-WHT", productName: "Dining Table Extendable / White Gloss", location: "Warehouse East", channel: "Retail Outlet A", status: "Preorder", availToPurchase: 0, availToBackorder: 0, availToPreorder: 90 },
    { skuCode: "R011-RUG-BLU", productName: "Abstract Area Rug / Blue & Grey / 8x10", location: "Warehouse West", channel: "Online Store", status: "Available", availToPurchase: 150, availToBackorder: 0, availToPreorder: 0 },
    { skuCode: "M013-MIRROR-GLD", productName: "Round Accent Mirror / Gold Frame", location: "Showroom Central", channel: "Retail Outlet B", status: "Available", availToPurchase: 60, availToBackorder: 5, availToPreorder: 10 },
    // Start of newly generated representative items (sample, should be ~88 more for 100 total)
    { skuCode: "GEN001-PAT-1234", productName: "Patio Chair / Metal / Charcoal / Outdoor", location: "Warehouse South", channel: "Mobile App", status: "Available", availToPurchase: 120, availToBackorder: 10, availToPreorder: 0 },
    { skuCode: "GEN002-BED-5678", productName: "Bed Frame / Pine / Natural / Classic", location: "Online Fulfillment Center", channel: "Online Store", status: "Low stock", availToPurchase: 35, availToBackorder: 5, availToPreorder: 0 },
    { skuCode: "GEN003-PLA-9012", productName: "Planter / Ceramic / White / Modern", location: "Retail Hub Metro", channel: "Partner Site", status: "Preorder", availToPurchase: 0, availToBackorder: 0, availToPreorder: 75 },
    { skuCode: "GEN004-NIG-3456", productName: "Nightstand / Walnut / Brown / Rustic", location: "Warehouse East", channel: "Retail Outlet A", status: "Backorder", availToPurchase: 22, availToBackorder: 30, availToPreorder: 10 },
    { skuCode: "GEN005-DRE-7890", productName: "Dresser / Oak / Grey / Minimalist", location: "Warehouse West", channel: "Online Store", status: "Available", availToPurchase: 90, availToBackorder: 0, availToPreorder: 0 },
    { skuCode: "GEN006-TVS-1230", productName: "TV Stand / Glass / Black / Industrial", location: "Showroom Central", channel: "Mobile App", status: "Discontinued", availToPurchase: 0, availToBackorder: 0, availToPreorder: 0 },
    { skuCode: "GEN007-OTT-4567", productName: "Ottoman / Velvet / Blue / Large", location: "Warehouse North", channel: "Retail Outlet B", status: "Low stock", availToPurchase: 55, availToBackorder: 15, availToPreorder: 5 },
    { skuCode: "GEN008-BAR-8901", productName: "Bar Stool / Leather / Silver / Tall", location: "Online Fulfillment Center", channel: "Online Store", status: "Available", availToPurchase: 150, availToBackorder: 25, availToPreorder: 0 },
    { skuCode: "GEN009-PAT-2345", productName: "Patio Chair / Plastic / Green / Kids", location: "Retail Hub Metro", channel: "Partner Site", status: "Preorder", availToPurchase: 0, availToBackorder: 0, availToPreorder: 60 },
    { skuCode: "GEN010-BED-6789", productName: "Bed Frame / Metal / Black / Modern", location: "Warehouse South", channel: "Online Store", status: "Available", availToPurchase: 110, availToBackorder: 0, availToPreorder: 0 },
    { skuCode: "GEN011-SHE-0123", productName: "Shelf / Concrete / Natural / Industrial", location: "Warehouse East", channel: "Retail Outlet A", status: "Backorder", availToPurchase: 40, availToBackorder: 60, availToPreorder: 20 },
    { skuCode: "GEN012-PLA-4560", productName: "Planter / Pine / Brown / Rustic", location: "Showroom Central", channel: "Online Store", status: "Low stock", availToPurchase: 25, availToBackorder: 5, availToPreorder: 0 },
    { skuCode: "GEN013-NIG-8900", productName: "Nightstand / Glass / Silver / Minimalist", location: "Warehouse West", channel: "Mobile App", status: "Available", availToPurchase: 70, availToBackorder: 10, availToPreorder: 0 }
    // ... Add approximately 75 more diverse entries here to reach a total of 100+ ...
];

function displayInventoryPage() {
    const mainContentArea = document.getElementById('main-content-area');
    if (!mainContentArea) return;

    mainContentArea.innerHTML = `
        <div class="inventory-container">
            <section class="inventory-table-section">
                <div class="inventory-table-header">
                     <h2>Inventory</h2> 
                </div>
                <div class="table-scroll-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>SKU <span class="sort-arrow">&#9662;</span></th>
                                <th>Location <span class="sort-arrow">&#9662;</span></th>
                                <th>Channel <span class="sort-arrow">&#9662;</span></th>
                                <th>Status <span class="sort-arrow">&#9662;</span></th>
                                <th>Avail. to Purchase <span class="sort-arrow">&#9662;</span></th>
                                <th>Avail. to Backorder <span class="sort-arrow">&#9662;</span></th>
                                <th>Avail. to Preorder <span class="sort-arrow">&#9662;</span></th>
                            </tr>
                        </thead>
                        <tbody>
                            ${mockInventoryData.map(item => `
                                <tr>
                                    <td>
                                        <div class="sku-cell">
                                            <div class="sku-details">
                                                <span class="sku-name-link">${item.productName}</span>
                                                <span class="sku-code">${item.skuCode}</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td>${item.location}</td>
                                    <td>${item.channel}</td>
                                    <td><span class="status-badge status-${item.status.toLowerCase().replace(' ', '-')}">${item.status}</span></td>
                                    <td>${item.availToPurchase}</td>
                                    <td>${item.availToBackorder}</td>
                                    <td>${item.availToPreorder}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    `;
}

// REMOVE the old hardcoded mockOrdersData constant.
// const mockOrdersData = [ ... old data ... ];

// --- Function to Display Orders Page (main table) ---
async function displayOrdersPage() { // Make it async
    const mainContentArea = document.getElementById('main-content-area');
    if (!mainContentArea) return;

    // Initial HTML with loading state
    mainContentArea.innerHTML = `
        <div class="orders-container">
            <section class="orders-main-content">
                <div class="orders-header">
                    <h2>Manage orders</h2>
                    <div class="orders-sub-nav">
                        <a href="#" class="active">Orders</a>
                        <a href="#">Allocation</a>
                        <a href="#">Shipment</a>
                        <a href="#">Invoice</a>
                    </div>
                </div>
                <div id="orders-table-area" class="loading-data">
                    <p>Loading orders...</p>
                </div>
            </section>
        </div>
    `;

    const ordersTableArea = document.getElementById('orders-table-area');

    try {
        const response = await fetch('http://localhost:5001/api/orders');
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: "Failed to fetch orders or parse error response."}));
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        const orders = await response.json();
        ordersTableArea.classList.remove('loading-data');

        if (orders && orders.length > 0) {
            let tableHTML = '<table><thead><tr><th>Order Number</th><th>Customer Name</th><th>Order Total</th><th>Order Status</th><th>Payment Status</th></tr></thead><tbody>';
            orders.forEach(order => {
                tableHTML += `
                    <tr>
                        <td><a href="#" class="order-number-link" data-order-id="${order.orderNumber}">${order.orderNumber}</a></td>
                        <td>
                            <div class="customer-details">
                                <span class="customer-name">${order.customerName || 'N/A'}</span>
                                <span class="customer-email">${order.customerEmail || 'N/A'}</span>
                            </div>
                        </td>
                        <td>${order.orderTotal || 'N/A'}</td>
                        <td><span class="status-badge status-${(order.orderStatus || 'unknown').toLowerCase().replace(/\s+/g, '-')}">${order.orderStatus || 'Unknown'}</span></td>
                        <td><span class="status-badge status-${(order.paymentStatus || 'unknown').toLowerCase().replace(/\s+/g, '-')}">${order.paymentStatus || 'Unknown'}</span></td>
                    </tr>
                `;
            });
            tableHTML += '</tbody></table>';
            ordersTableArea.innerHTML = tableHTML;

            // Re-attach event listeners to newly created order number links
            ordersTableArea.querySelectorAll('.order-number-link').forEach(link => {
                link.addEventListener('click', (event) => {
                    event.preventDefault();
                    const orderId = event.target.dataset.orderId;
                    if (orderId) {
                        displayOrderDetailsPage(orderId);
                    }
                });
            });

        } else {
            ordersTableArea.innerHTML = '<p>No orders found.</p>';
        }

    } catch (error) {
        console.error("Error fetching orders:", error);
        ordersTableArea.classList.remove('loading-data');
        ordersTableArea.innerHTML = `<p class="error-message">Error loading orders: ${error.message}</p>`;
    }
}

// --- Function to Display Order Details Page ---
async function displayOrderDetailsPage(orderId) {
    const mainContentArea = document.getElementById('main-content-area');
    if (!mainContentArea) return;

    mainContentArea.innerHTML = '<div class="order-details-loading"><p>Loading order details...</p></div>';

    try {
        const response = await fetch(`http://localhost:5001/api/orders/${orderId}`);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: "Order not found or failed to parse error." }));
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        const order = await response.json();
        
        const generateProgressBar = (statusProgress) => {
            const allSteps = ["Created", "Allocated", "Picked Up", "Shipped", "Delivered"]; 
            let html = '<div class="progress-bar-container">';
            allSteps.forEach((step, index) => {
                const isCompleted = statusProgress.includes(step);
                const isActive = isCompleted && (index === statusProgress.length -1) && (statusProgress.length < allSteps.length);

                html += `<div class="progress-step ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}">
                            <div class="progress-dot"></div>
                            <div class="progress-label">${step}</div>
                        </div>`;
                if (index < allSteps.length - 1) {
                    html += `<div class="progress-connector ${statusProgress.length > index ? 'completed' : ''}"></div>`;
                }
            });
            html += '</div>';
            return html;
        };

        let orderDetailsHTML = `
            <div class="order-details-page">
                <header class="order-details-header">
                    <h1>Order ${order.displayOrderId || order.orderId}</h1>
                    <span class="status-badge status-${(order.status || 'unknown').toLowerCase().replace(/\s+/g, '-')}">${order.status || 'Unknown'}</span>
                </header>
                <nav class="order-details-sub-nav">
                    <a href="#" class="active">Basic details</a>
                    <a href="#">Allocations</a>
                    <a href="#">Shipments</a>
                    <a href="#">Invoices</a>
                    <a href="#">Activity log</a>
                </nav>
                <div class="order-details-body">
                    <section class="order-info-main">
                        <div class="order-basic-info">
                            <div><strong>Order ID:</strong> ${order.internalOrderId || 'N/A'}</div>
                            <div><strong>Order type:</strong> ${order.orderType || 'N/A'}</div>
                            <div><strong>Date Created:</strong> ${order.dateCreated || 'N/A'}</div>
                        </div>
                        <a href="#" class="view-more-attributes-link">View more attributes</a>
                        ${(order.shippingGroups && order.shippingGroups.length > 0) ? 
                            order.shippingGroups.map(group => `
                                <div class="order-status-section">
                                    <div class="section-header">
                                        <h3>Order Status</h3>
                                        <span class="collapse-arrow">&#9660;</span>
                                    </div>
                                    <div class="shipping-group">
                                        <h4>${group.groupTitle || 'Shipping Group'} <span class="status-badge status-type-${(group.type || '').toLowerCase()}">${group.type}</span></h4>
                                        ${group.type === 'Pick Up' && group.pickupDetails ? `
                                            <div class="pickup-info">
                                                <p><strong>Pick up details</strong></p>
                                                <p>Pick up by: ${group.pickupDetails.pickUpBy || 'N/A'}</p>
                                                <p>Pick up location: ${group.pickupDetails.pickUpLocation || 'N/A'}</p>
                                            </div>
                                        ` : ''}
                                        ${group.type === 'Delivery' && group.deliveryAddress ? `
                                            <div class="delivery-info">
                                                <p><strong>Delivery Address:</strong> ${group.deliveryAddress || 'N/A'}</p>
                                            </div>
                                        ` : ''}
                                        ${(group.lineItems && group.lineItems.length > 0) ? group.lineItems.map(item => {
                                            const currencySymbol = item.currency === 'USD' ? '$' : (item.currency || '');
                                            return `
                                            <div class="line-item">
                                                <div class="line-item-details">
                                                    <span class="line-item-sku">${item.sku}</span>
                                                    <span class="line-item-name">${item.productName || 'N/A'}</span>
                                                    <span class="line-item-qty">Qty: ${item.quantity || 1}</span>
                                                    <span class="line-item-total">Total: ${currencySymbol}${item.itemTotal || 'N/A'}</span>
                                                </div>
                                                <div class="line-item-progress">
                                                    ${generateProgressBar(item.statusProgress || [])}
                                                </div>
                                            </div>
                                        `}).join('') : '<p>No line items in this group.</p>'}
                                    </div>
                                </div>
                            `).join('') : '<p>No shipping groups for this order.</p>'}
                    </section>
                    <aside class="order-summary-sidebar">
                        <h3>Order Summary</h3>
                        ${order.orderSummary ? `
                            <div class="summary-item"><span>Subtotal:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.subtotal || '0.00'}</span></div>
                            <div class="summary-item"><span>Discount:</span> <span>-${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.discount || '0.00'}</span></div>
                            <div class="summary-item"><span>Shipping:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.shipping || '0.00'}</span></div>
                            <div class="summary-item"><span>Fees:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.fees || '0.00'}</span></div>
                            <div class="summary-item"><span>Adjustments:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.adjustments || '0.00'}</span></div>
                            <div class="summary-item"><span>Taxes:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.taxes || '0.00'}</span></div>
                            <div class="summary-item total"><span>Total:</span> <span>${order.orderSummary.currency === 'USD' ? '$' : (order.orderSummary.currency || '')}${order.orderSummary.total || '0.00'}</span></div>
                        ` : '<p>Summary not available.</p>'}
                    </aside>
                </div>
            </div>
        `;
        mainContentArea.innerHTML = orderDetailsHTML;

    } catch (error) {
        console.error("Error fetching order details:", error);
        mainContentArea.innerHTML = `<p class="error-message">Error loading order details: ${error.message}</p>`;
    }
}

// --- Function to Display Home Page ---
function displayHomePage() {
    const mainContentArea = document.getElementById('main-content-area');
    if (!mainContentArea) return;

    mainContentArea.innerHTML = `
        <div class="home-container">
            <div class="welcome-message">
                <h1>Hello. Welcome to fabric!</h1>
            </div>
        </div>
    `;

    // JavaScript for the central chat interface (input, send button, message handling)
    // has been REMOVED from this function as it's no longer part of the Home page directly.
    // The Fabric Intelligence sidebar chat handles chat functionality now.
}

// --- Function to Display Customers Page ---
async function displayCustomersPage() {
    const mainContentArea = document.getElementById('main-content-area');
    if (!mainContentArea) return;

    mainContentArea.innerHTML = `
        <div class="customers-container">
            <h2>Customers</h2>
            <div id="customer-list-area" class="loading-data">
                <p>Loading customer data...</p>
            </div>
        </div>
    `;

    const customerListArea = document.getElementById('customer-list-area');

    try {
        const response = await fetch('http://localhost:5001/api/customers');
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: "Failed to fetch customer data or parse error response."}));
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        const customers = await response.json();
        customerListArea.classList.remove('loading-data');

        if (customers && customers.length > 0) {
            let customersHTML = '<table class="customers-table">';
            customersHTML += '<thead><tr><th>Name</th><th>Email</th><th>ZIP Code</th><th>Tier</th></tr></thead><tbody>';
            customers.forEach(customer => {
                customersHTML += `
                    <tr>
                        <td>${customer.name || 'N/A'}</td>
                        <td>${customer.email || 'N/A'}</td>
                        <td>${customer.zipCode || 'N/A'}</td>
                        <td><span class="status-badge status-tier-${(customer.tier || 'standard').toLowerCase()}">${customer.tier || 'Standard'}</span></td>
                    </tr>
                `;
            });
            customersHTML += '</tbody></table>';
            customerListArea.innerHTML = customersHTML;
        } else {
            customerListArea.innerHTML = '<p>No customer data found.</p>';
        }
    } catch (error) {
        console.error("Error fetching customer data:", error);
        customerListArea.classList.remove('loading-data');
        customerListArea.innerHTML = `<p class="error-message">Error loading customer data: ${error.message}</p>`;
    }
}

// --- Initialize Fabric Intelligence Chat Sidebar ---
function initializeFabricIntelligenceChat() {
    const chatInput = document.getElementById('fi-chat-input');
    const sendChatButton = document.getElementById('fi-send-chat-button');
    const chatMessagesArea = document.getElementById('fi-chat-messages-area');
    let fiChatHistory = [];

    if (!chatInput || !sendChatButton || !chatMessagesArea) {
        console.warn("Fabric Intelligence chat elements not found. Skipping initialization.");
        return;
    }

    const addMessageToFiChat = (message, sender, isHTML = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('fi-chat-message', sender === 'user' ? 'user-message' : 'agent-message'); 
        
        let messageContent = message;
        if (isHTML) {
            messageDiv.innerHTML = message;
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = message;
            messageContent = tempDiv.textContent || tempDiv.innerText || ""; 
        } else {
            messageDiv.textContent = message;
        }
        chatMessagesArea.appendChild(messageDiv);
        chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;

        const historyRole = (sender === 'user') ? 'user' : 'assistant';

        if (!(sender === 'assistant' && message.includes("Working on that"))) {
             fiChatHistory.push({ role: historyRole, content: messageContent.trim() });
        }
        // console.log("Updated FI History:", fiChatHistory); 

        messageDiv.querySelectorAll('.fi-suggestion-button').forEach(button => {
            button.addEventListener('click', () => {
                const suggestionText = button.closest('.fi-chat-message').querySelector('strong')?.textContent || "a suggestion";
                const userConfirmation = `Okay, I will try to apply suggestion: "${suggestionText}"`;
                addMessageToFiChat(userConfirmation, 'user');
                callFabricIntelligenceAPIwithHistory(`Apply suggestion: ${suggestionText}`); 
            });
        });
    };

    async function callFabricIntelligenceAPIwithHistory(currentQuery) {
        const thinkingMessageDiv = document.createElement('div');
        thinkingMessageDiv.classList.add('fi-chat-message', 'agent-message', 'working');
        thinkingMessageDiv.innerHTML = '<span class="fi-spinner"></span> Working on that.';
        chatMessagesArea.appendChild(thinkingMessageDiv);
        chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
        
        try {
            const response = await fetch('http://localhost:5001/api/fabric-intelligence-chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ messages: fiChatHistory }) 
            });

            chatMessagesArea.removeChild(thinkingMessageDiv);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: "Failed to parse error response from server." }));
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (data.response) {
                addMessageToFiChat(data.response, 'assistant');
            } else if (data.error) {
                addMessageToFiChat(`Error from agent: ${data.error}`, 'assistant');
            } else {
                addMessageToFiChat("Received an unexpected response from the agent.", 'assistant');
            }
        } catch (error) {
            if (chatMessagesArea.contains(thinkingMessageDiv)) {
                chatMessagesArea.removeChild(thinkingMessageDiv);
            }
            console.error("Error calling Fabric Intelligence API:", error);
            addMessageToFiChat(`Sorry, I encountered an error: ${error.message}`, 'assistant');
        }
    }

    sendChatButton.addEventListener('click', () => {
        const message = chatInput.value.trim();
        if (message) {
            addMessageToFiChat(message, 'user'); 
            chatInput.value = '';
            callFabricIntelligenceAPIwithHistory(); 
        }
    });

    chatInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendChatButton.click();
        }
    });

    const initialMessages = chatMessagesArea.querySelectorAll('.fi-chat-message');
    initialMessages.forEach(msg => msg.remove());
    fiChatHistory = []; 
    addMessageToFiChat("Hi there! How can I help you with Fabric Intelligence today?", 'assistant');

}

// --- Update DOMContentLoaded to include Home link and set default view ---
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = {
        home: document.getElementById('main-nav-home'),
        inventory: document.getElementById('main-nav-inventory'),
        orders: document.getElementById('main-nav-orders'),
        customers: document.getElementById('main-nav-customers')
    };

    const allNavLiElements = Object.values(navLinks).filter(el => el).map(el => el.closest('li'));

    function setActiveNav(selectedPage) {
        allNavLiElements.forEach(li => li.classList.remove('active'));
        if (navLinks[selectedPage] && navLinks[selectedPage].closest('li')) {
            navLinks[selectedPage].closest('li').classList.add('active');
        }
    }

    if (navLinks.home) {
        navLinks.home.addEventListener('click', (event) => {
            event.preventDefault();
            displayHomePage();
            setActiveNav('home');
        });
    }

    if (navLinks.inventory) {
        navLinks.inventory.addEventListener('click', (event) => {
            event.preventDefault();
            displayInventoryPage();
            setActiveNav('inventory');
        });
    }

    if (navLinks.orders) {
        // The click target is the span inside the li for Orders
        const ordersLabel = navLinks.orders.querySelector('.nav-item-label');
        if (ordersLabel) {
            ordersLabel.addEventListener('click', (event) => {
                event.preventDefault();
                displayOrdersPage(); // This still loads the "Manage Orders" table view
                setActiveNav('orders');
            });
        } else { // Fallback if span isn't there, click the LI
             navLinks.orders.addEventListener('click', (event) => {
                event.preventDefault();
                displayOrdersPage();
                setActiveNav('orders');
            });
        }
    }

    if (navLinks.customers) {
        navLinks.customers.addEventListener('click', (event) => {
            event.preventDefault();
            displayCustomersPage();
            setActiveNav('customers');
        });
    }

    // Initialize the Fabric Intelligence Chat
    initializeFabricIntelligenceChat();

    // Set initial active state for main navigation and display home page
    displayHomePage(); 
    setActiveNav('home');
}); 