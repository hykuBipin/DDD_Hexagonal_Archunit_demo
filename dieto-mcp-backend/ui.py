HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dieto AI Health & Calorie Caretaker</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #FC8019; /* Swiggy Orange */
            --bg-main: #f4f6f8;
            --bg-card: #ffffff;
            --text-main: #1c1c1c;
            --text-muted: #686b78;
            --shadow: 0 8px 30px rgba(0,0,0,0.06);
            --dark-glass: rgba(30, 30, 30, 0.96);
            --border-color: #e9e9eb;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        header {
            background-color: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 16px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .logo-swiggy {
            color: var(--primary);
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .logo-dieto {
            background: linear-gradient(135deg, #10B981, #059669);
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }

        .address-badge {
            color: var(--text-muted);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .container {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 32px;
            max-width: 1320px;
            margin: 32px auto;
            width: 100%;
            padding: 0 24px;
            flex-grow: 1;
        }

        .panel-left {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .card-setup {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .setup-row {
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 20px;
        }

        .setup-field {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .setup-label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
        }

        .setup-input {
            padding: 10px 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }

        .preferences-checklist {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .pref-checkbox-label {
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }

        .menu-section {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .menu-card {
            background-color: var(--bg-card);
            border-radius: 8px;
            padding: 16px;
            border: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow);
        }

        .menu-details {
            max-width: 65%;
        }

        .menu-name {
            font-size: 14px;
            font-weight: 600;
        }

        .menu-meta {
            font-size: 11px;
            color: var(--text-muted);
            margin: 4px 0;
        }

        .btn-add-item {
            border: 1px solid var(--border-color);
            background-color: white;
            color: #60B246;
            padding: 6px 14px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 12px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        }

        .btn-add-item:hover {
            background-color: #f9f9f9;
        }

        .panel-right {
            background-color: var(--dark-glass);
            border-radius: 16px;
            padding: 28px;
            color: #ffffff;
            box-shadow: 0 16px 50px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
            gap: 24px;
            height: fit-content;
        }

        .dieto-header {
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .dieto-title {
            font-size: 18px;
            font-weight: 600;
            color: #10B981;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .profile-tracker-box {
            background-color: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 8px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .progress-container {
            background-color: rgba(255,255,255,0.1);
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
        }

        .progress-bar {
            background: linear-gradient(90deg, #10B981, #F59E0B);
            width: 0%;
            height: 100%;
            border-radius: 6px;
            transition: width 0.3s;
        }

        .progress-bar.excessive {
            background: linear-gradient(90deg, #F59E0B, #EF4444);
        }

        .caretaker-tip-card {
            background-color: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            font-size: 13px;
        }

        .caretaker-title {
            color: #10B981;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .caretaker-desc {
            color: rgba(255,255,255,0.9);
            line-height: 1.4;
        }

        .caretaker-rec-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            padding: 8px 12px;
            margin-top: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-order {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: all 0.15s;
        }

        .btn-order:hover {
            background-color: #e06c11;
        }

        .terminal-panel {
            background-color: #0b0b0b;
            border-radius: 8px;
            padding: 14px;
            font-family: monospace;
            font-size: 11px;
            color: #00FF66;
            max-height: 130px;
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.04);
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .post-order-panel {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 24px;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            display: none;
            flex-direction: column;
            gap: 16px;
        }

        .post-order-title {
            font-size: 16px;
            font-weight: 600;
        }

        .comparison-badge {
            background-color: rgba(16, 185, 129, 0.1);
            color: #10B981;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 500;
            width: fit-content;
        }

        .comparison-badge.warn {
            background-color: rgba(239, 68, 68, 0.1);
            color: #EF4444;
        }

        .btn-scan {
            background-color: #10B981;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            align-self: flex-start;
        }
    </style>
</head>
<body>

<header>
    <div class="logo-section">
        <span class="logo-swiggy">Swiggy</span>
        <span class="logo-dieto">Dieto Caretaker AI</span>
    </div>
    <div class="address-badge">
        📍 <strong>Delivery Address</strong> - Indiranagar, Bangalore
    </div>
</header>

<div class="container">
    <!-- Left Column: Setup & Menu -->
    <div class="panel-left">
        <!-- Diner setup & history preferences -->
        <div class="card-setup">
            <h3 style="font-size: 16px; font-weight: 600;">Diner Profile & Dietary Preferences</h3>
            <div class="setup-row">
                <div class="setup-field">
                    <span class="setup-label">User Profile Name</span>
                    <input type="text" id="userNameInput" class="setup-input" value="Bipin" oninput="updateTrackers()">
                </div>
                <div class="setup-field">
                    <span class="setup-label">Dietary Target Mode</span>
                    <select id="dietTargetMode" onchange="updateTrackers()" class="setup-input" style="padding: 9px 12px; background: white; cursor: pointer;">
                        <option value="strict">Strict Mode (1,600 kcal limit)</option>
                        <option value="balanced" selected>Balanced Mode (2,000 kcal limit)</option>
                        <option value="relaxed">Relaxed Mode (2,800 kcal limit)</option>
                    </select>
                </div>
            </div>
            
            <div class="setup-field" style="margin-top: 6px;">
                <span class="setup-label">Dietary History & Allergy Preferences</span>
                <div class="preferences-checklist">
                    <label class="pref-checkbox-label">
                        <input type="checkbox" id="chkNoSugar" onchange="updateTrackers()" checked> 🚫 No Added Sugar
                    </label>
                    <label class="pref-checkbox-label">
                        <input type="checkbox" id="chkNoGarlic" onchange="updateTrackers()"> 🧄 No Garlic / Onion
                    </label>
                    <label class="pref-checkbox-label">
                        <input type="checkbox" id="chkGlutenFree" onchange="updateTrackers()"> 🌾 Gluten-Free
                    </label>
                </div>
            </div>
        </div>

        <!-- Menu Section -->
        <div class="menu-section">
            <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">Swiggy Food Menu</h3>
            <div class="menu-grid" id="menuGrid">
                <!-- Menu cards dynamically loaded -->
            </div>
        </div>

        <!-- Post Order Plate Verification Scanner -->
        <div class="post-order-panel" id="postOrderPanel">
            <div class="post-order-title">🍽️ Post-Delivery Plate Scanner</div>
            <div id="comparisonBadge" class="comparison-badge">Awaiting delivery...</div>
            <p style="font-size: 13px; color: var(--text-muted);">
                When your delivery arrives, take a quick photo. Dieto verifies portion sizes to ensure you stay aligned comfortably without restrictive limits:
            </p>
            <div id="plateScanDetails" style="font-size: 13px; line-height: 1.5; color: var(--text-main); margin: 6px 0;"></div>
            <div id="plateScanAdvice" style="display:flex; flex-direction:column; gap:8px;"></div>
            <button class="btn-scan" onclick="triggerSimulatedScan()">📷 Scan Delivery Plate & Verify Portion</button>
        </div>
    </div>

    <!-- Right Column: Dieto Caretaker Advice Panel -->
    <div class="panel-right">
        <div class="dieto-header">
            <div class="dieto-title">🥗 Dieto Caloric Tracker</div>
            <span style="font-size: 12px; color: rgba(255,255,255,0.6);">Encouraging Health Assistant</span>
        </div>

        <!-- Progress Tracker box -->
        <div class="profile-tracker-box">
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600;">
                <span id="trackerName">Bipin's Daily Intake</span>
                <span id="trackerTargetVal">1,200 / 2,000 kcal</span>
            </div>
            
            <div class="progress-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.7);">
                <span id="remainingVal">Remaining Budget: 800 kcal</span>
                <span id="modeLabel">Balanced Mode</span>
            </div>
        </div>

        <!-- Positive Caretaker Tips Card -->
        <div class="caretaker-tip-card">
            <div class="caretaker-title">🌟 Dieto Caretaker Tip</div>
            <div class="caretaker-desc" id="caretakerHeaderDesc">
                Food is joy and fuel! We encourage you to enjoy your meal. Here are encouraging wellness tips based on your menu selection and profile preferences:
            </div>
            <div id="caretakerTipsList" style="display: flex; flex-direction: column; gap: 8px;">
                <!-- dynamic tips list loaded here -->
            </div>
        </div>

        <!-- Checkout Button -->
        <button class="btn-order" id="btnPlaceOrder" onclick="checkoutOrder()">Place Swiggy Order (0 kcal)</button>

        <!-- Console MCP JSON-RPC Output -->
        <div class="terminal-panel" id="mcpTerminal">
            [MCP System] Ready. Select menu items to analyze.
        </div>
    </div>
</div>

<script>
    // App States
    let baseCalories = 1200;
    let targetCalories = 2000;
    let selectedItem = null;
    let orderPlacedId = "";

    const MENU_ITEMS = [
        { name: "Chicken Tikka Wrap", calories: 480, price: 180 },
        { name: "Paneer Rice Bowl", calories: 560, price: 210 },
        { name: "Double Cheese Burger", calories: 680, price: 240 },
        { name: "Tandoori Chicken Salad", calories: 350, price: 220 },
        { name: "Lime Soda", calories: 120, price: 60 },
        { name: "Mint Juice", calories: 45, price: 80 }
    ];

    function logTerminal(msg) {
        const console = document.getElementById('mcpTerminal');
        const time = new Date().toLocaleTimeString();
        console.innerHTML += `<br>[${time}] ${msg}`;
        console.scrollTop = console.scrollHeight;
    }

    // Load Menu
    function loadMenu() {
        const grid = document.getElementById('menuGrid');
        grid.innerHTML = '';
        MENU_ITEMS.forEach(item => {
            const card = document.createElement('div');
            card.className = 'menu-card';
            card.innerHTML = `
                <div class="menu-details">
                    <div class="menu-name">${item.name}</div>
                    <div class="menu-meta">₹${item.price} | 🔥 ${item.calories} kcal</div>
                </div>
                <button class="btn-add-item" onclick="addItem('${item.name}', ${item.calories})">+ ADD</button>
            `;
            grid.appendChild(card);
        });
    }

    function addItem(name, calories) {
        selectedItem = { name, calories };
        logTerminal(`[MCP] Call: update_food_cart("add":"${name}") -> Synced`);
        updateTrackers();
    }

    function updateTrackers() {
        const name = document.getElementById('userNameInput').value || 'User';
        const mode = document.getElementById('dietTargetMode').value;
        
        // Mode Thresholds
        targetCalories = mode === 'strict' ? 1600 : (mode === 'balanced' ? 2000 : 2800);
        
        document.getElementById('trackerName').innerText = `${name}'s Daily Intake`;
        document.getElementById('modeLabel').innerText = mode.charAt(0).toUpperCase() + mode.slice(1) + " Mode";

        const addedCalories = selectedItem ? selectedItem.calories : 0;
        const totalProjected = baseCalories + addedCalories;

        const bar = document.getElementById('progressBar');
        const percent = Math.min(100, (totalProjected / targetCalories) * 100);
        bar.style.width = `${percent}%`;

        if (totalProjected > targetCalories) {
            bar.classList.add('excessive');
        } else {
            bar.classList.remove('excessive');
        }

        document.getElementById('trackerTargetVal').innerText = `${totalProjected} / ${targetCalories} kcal`;
        const remaining = targetCalories - totalProjected;
        document.getElementById('remainingVal').innerText = remaining >= 0 ? `Remaining Budget: ${remaining} kcal` : `Over Budget by: ${Math.abs(remaining)} kcal`;

        // Update checkout button text
        const btn = document.getElementById('btnPlaceOrder');
        btn.innerText = `Place Swiggy Order (${addedCalories} kcal)`;

        // Fetch dynamic recovery advisor tips from backend API
        const noSugar = document.getElementById('chkNoSugar').checked;
        const noGarlic = document.getElementById('chkNoGarlic').checked;
        const glutenFree = document.getElementById('chkGlutenFree').checked;

        const excess = totalProjected > targetCalories ? (totalProjected - targetCalories) : 0;

        fetch('/recovery', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                excess_calories: excess,
                no_sugar: noSugar,
                no_garlic: noGarlic,
                gluten_free: glutenFree
            })
        })
        .then(r => r.json())
        .then(data => {
            const listDiv = document.getElementById('caretakerTipsList');
            listDiv.innerHTML = '';
            
            data.recommendations.forEach(rec => {
                const div = document.createElement('div');
                div.className = 'caretaker-rec-item';
                div.innerText = rec;
                listDiv.appendChild(div);
            });
        });
    }

    function checkoutOrder() {
        if (!selectedItem) {
            logTerminal("[SYSTEM] Cart is empty. Add a dish from the Swiggy Menu.");
            return;
        }
        logTerminal("[MCP] Launching Swiggy Food MCP checkout flow...");
        document.getElementById('btnPlaceOrder').disabled = true;

        setTimeout(() => {
            logTerminal("[MCP] Call: get_addresses() -> Completed (200 OK)");
            
            setTimeout(() => {
                logTerminal("[MCP] Call: update_food_cart() -> Completed (200 OK)");
                
                setTimeout(() => {
                    logTerminal("[MCP] Call: place_food_order() -> Completed (200 OK)");
                    const orderId = "ord_swiggy_7711";
                    orderPlacedId = orderId;
                    logTerminal(`[MCP] Success! Order completed. Order ID: ${orderId}`);
                    logTerminal("[SYSTEM] Swiggy Order Completed successfully!");

                    // Sync base calories with FastAPI
                    fetch('/sync-order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ order_id: orderId })
                    })
                    .then(r => r.json())
                    .then(data => {
                        baseCalories += selectedItem.calories;
                        selectedItem = null;
                        updateTrackers();
                        
                        // Show Plate verification scanner panel
                        document.getElementById('postOrderPanel').style.display = 'flex';
                        document.getElementById('comparisonBadge').innerText = "Delivery on the way... 🛵";
                    });
                }, 800);
            }, 600);
        }, 800);
    }

    function triggerSimulatedScan() {
        if (!orderPlacedId) return;
        document.getElementById('comparisonBadge').innerText = "📷 Scanning plate portions...";

        const noSugar = document.getElementById('chkNoSugar').checked;
        const noGarlic = document.getElementById('chkNoGarlic').checked;
        const glutenFree = document.getElementById('chkGlutenFree').checked;

        setTimeout(() => {
            fetch('/compare-plate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    order_id: orderPlacedId,
                    detected_items: ["Chicken Biryani", "Chicken 65", "Raita"],
                    no_sugar: noSugar,
                    no_garlic: noGarlic,
                    gluten_free: glutenFree
                })
            })
            .then(r => r.json())
            .then(data => {
                const badge = document.getElementById('comparisonBadge');
                badge.innerText = data.calorie_difference > 0 ? "Portion Divergence Scanned (+280 kcal)" : "Intake Budget Met!";
                badge.className = data.calorie_difference > 0 ? "comparison-badge warn" : "comparison-badge";

                const details = document.getElementById('plateScanDetails');
                details.innerHTML = `<strong>Swiggy Est</strong>: 1000 kcal<br>` +
                                    `<strong>Plate Scanned Est</strong>: 1280 kcal<br>` +
                                    `<strong>Divergence</strong>: +280 kcal`;

                const adviceDiv = document.getElementById('plateScanAdvice');
                adviceDiv.innerHTML = '<strong>Caretaker Guidelines</strong>:';
                data.coach_advice.recommendations.forEach(rec => {
                    const div = document.createElement('div');
                    div.className = 'caretaker-rec-item';
                    div.style.background = 'rgba(0, 0, 0, 0.03)';
                    div.innerText = rec;
                    adviceDiv.appendChild(div);
                });
            });
        }, 1200);
    }

    // Init onload
    window.onload = () => {
        loadMenu();
        updateTrackers();
    }
</script>

</body>
</html>
"""
