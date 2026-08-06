HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swiggy OrderTogether & Dieto Caretaker Simulator</title>
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
            grid-template-columns: 1.15fr 0.85fr;
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
            grid-template-columns: 1fr 1fr;
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

        .btn-match {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            text-align: center;
            transition: background-color 0.15s;
        }

        .btn-match:hover {
            background-color: #e06c11;
        }

        .matched-restaurants {
            display: none;
            flex-direction: column;
            gap: 12px;
        }

        .restaurant-row {
            background-color: var(--bg-card);
            border-radius: 8px;
            padding: 16px;
            border: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.15s;
        }

        .restaurant-row.selected {
            border-color: var(--primary);
            background-color: rgba(252, 128, 25, 0.03);
            box-shadow: 0 4px 12px rgba(252,128,25,0.06);
        }

        .restaurant-details {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .restaurant-name {
            font-size: 16px;
            font-weight: 600;
        }

        .restaurant-meta {
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            gap: 12px;
        }

        .menu-section {
            display: none;
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

        .diner-profile-box {
            background-color: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .diner-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .diner-name {
            font-size: 14px;
            font-weight: 600;
        }

        .progress-container {
            background-color: rgba(255,255,255,0.1);
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
        }

        .progress-bar {
            background: linear-gradient(90deg, #10B981, #F59E0B);
            width: 0%;
            height: 100%;
            border-radius: 5px;
            transition: width 0.3s;
        }

        .progress-bar.excessive {
            background: linear-gradient(90deg, #F59E0B, #EF4444);
        }

        .caretaker-tip-box {
            background-color: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 6px;
            padding: 12px;
            display: none;
            flex-direction: column;
            gap: 8px;
            font-size: 12px;
        }

        .caretaker-title {
            color: #F59E0B;
            font-weight: 600;
        }

        .caretaker-desc {
            color: rgba(255,255,255,0.85);
            line-height: 1.4;
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
        }

        .btn-order:disabled {
            background-color: rgba(255,255,255,0.08);
            color: rgba(255,255,255,0.25);
            cursor: not-allowed;
        }

        .terminal-panel {
            background-color: #0b0b0b;
            border-radius: 8px;
            padding: 14px;
            font-family: monospace;
            font-size: 11px;
            color: #00FF66;
            max-height: 120px;
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
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            width: fit-content;
        }

        .comparison-badge.warn {
            background-color: rgba(239, 68, 68, 0.1);
            color: #EF4444;
        }

        .suggestion-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 13px;
            color: var(--text-muted);
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
        <span class="logo-swiggy">OrderTogether</span>
        <span class="logo-dieto">Dieto Caretaker</span>
    </div>
    <div class="address-badge">
        📍 <strong>Diner Group Address</strong> - Indiranagar, Bangalore
    </div>
</header>

<div class="container">
    <!-- Left Column: Setup and Menu MATCH -->
    <div class="panel-left">
        <!-- Diner profiles setup -->
        <div class="card-setup">
            <h3 style="font-size: 16px; font-weight: 600;">Diner Preference Setup</h3>
            <div class="setup-row">
                <div class="setup-field">
                    <span class="setup-label">Diner 1 Name</span>
                    <input type="text" id="diner1Name" class="setup-input" value="Bipin">
                </div>
                <div class="setup-field">
                    <span class="setup-label">Diner 1 Dish Preference</span>
                    <input type="text" id="diner1Pref" class="setup-input" value="shawarma">
                </div>
            </div>
            <div class="setup-row">
                <div class="setup-field">
                    <span class="setup-label">Diner 2 Name</span>
                    <input type="text" id="diner2Name" class="setup-input" value="Sahan">
                </div>
                <div class="setup-field">
                    <span class="setup-label">Diner 2 Dish Preference</span>
                    <input type="text" id="diner2Pref" class="setup-input" value="dal tadka">
                </div>
            </div>
            <button class="btn-match" onclick="findMatchedRestaurants()">Find Joint Restaurants on Swiggy</button>
        </div>

        <!-- Matched restaurants row list -->
        <div class="matched-restaurants" id="matchedRestaurantsSection">
            <h3 style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">Matched Restaurants (Intersections)</h3>
            <div class="restaurant-row" id="restJunctionRow" onclick="selectRestaurant('rest_junction')">
                <div class="restaurant-details">
                    <span class="restaurant-name">Indian Spice Junction</span>
                    <div class="restaurant-meta">
                        <span>⭐ 4.6</span>
                        <span>🕒 30 mins</span>
                        <span style="color: #60B246;">Fits: shawarma, dal tadka, wraps</span>
                    </div>
                </div>
                <span style="font-size: 12px; font-weight: 600; color: var(--primary);">SELECT RESTAURANT</span>
            </div>
        </div>

        <!-- Selected Restaurant Menu Grid -->
        <div class="menu-section" id="menuSection">
            <h3 id="selectedRestHeader" style="font-size: 16px; font-weight: 600; margin-bottom: 4px;">Menu</h3>
            <div class="menu-grid" id="menuGrid">
                <!-- menu items injected here -->
            </div>
        </div>

        <!-- Post Order verification section -->
        <div class="post-order-panel" id="postOrderPanel">
            <div class="post-order-title">🍽️ Post-Order Joint Plate Scanner</div>
            <div id="comparisonBadge" class="comparison-badge">Awaiting delivery scan...</div>
            <p style="font-size: 13px; color: var(--text-muted);">
                Take a photograph of your delivered plates. Dieto compares original order calories vs portion sizes to trigger coach suggestions:
            </p>
            <div id="plateScanDetails" style="font-size: 13px; line-height: 1.5; color: var(--text-main);"></div>
            <div class="suggestion-list" id="wellnessAdviceList"></div>
            <button class="btn-scan" onclick="triggerSimulatedScan()">📷 Scan & Verify Plate Portions</button>
        </div>
    </div>

    <!-- Right Column: Dieto Caretaker dashboard -->
    <div class="panel-right">
        <div class="dieto-header">
            <div class="dieto-title">🥗 Dieto Calorimeter</div>
            <span style="font-size: 12px; color: rgba(255,255,255,0.6);">Joint Dining Mode</span>
        </div>

        <!-- Diner 1 tracker -->
        <div class="diner-profile-box">
            <div class="diner-header">
                <span class="diner-name" id="labelDiner1">Bipin (Diner 1)</span>
                <select id="modeDiner1" onchange="updateTrackers()" style="background: rgba(255,255,255,0.08); color: white; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; font-size: 10px; outline: none; padding: 2px 4px;">
                    <option value="strict">Strict Mode (1600 kcal)</option>
                    <option value="balanced" selected>Balanced Mode (2000 kcal)</option>
                    <option value="relaxed">Relaxed Mode (2800 kcal)</option>
                </select>
            </div>
            <div style="display:flex; justify-content:space-between; font-size: 12px;">
                <span>Calories Intake</span>
                <span id="valDiner1">1,420 / 2,000 kcal</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" id="barDiner1"></div>
            </div>
            <!-- Caretaker tips for diner 1 -->
            <div class="caretaker-tip-box" id="tipDiner1">
                <div class="caretaker-title">ℹ️ Dieto Caretaker Tip (Bipin)</div>
                <div class="caretaker-desc" id="descDiner1">
                    Your dish choice puts you above your daily budget. Don't worry! We suggest:
                </div>
                <label class="checkbox-container" style="margin-top: 6px;">
                    <input type="checkbox" id="swapDiner1" onchange="applySwapDiner1()">
                    🔄 Neutralize: Swap Shawarma for Wheat Wrap (-130 kcal)
                </label>
            </div>
        </div>

        <!-- Diner 2 tracker -->
        <div class="diner-profile-box">
            <div class="diner-header">
                <span class="diner-name" id="labelDiner2">Sahan (Diner 2)</span>
                <select id="modeDiner2" onchange="updateTrackers()" style="background: rgba(255,255,255,0.08); color: white; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; font-size: 10px; outline: none; padding: 2px 4px;">
                    <option value="strict">Strict Mode (1600 kcal)</option>
                    <option value="balanced" selected>Balanced Mode (2000 kcal)</option>
                    <option value="relaxed">Relaxed Mode (2800 kcal)</option>
                </select>
            </div>
            <div style="display:flex; justify-content:space-between; font-size: 12px;">
                <span>Calories Intake</span>
                <span id="valDiner2">1,580 / 2,000 kcal</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" id="barDiner2"></div>
            </div>
            <!-- Caretaker tips for diner 2 -->
            <div class="caretaker-tip-box" id="tipDiner2">
                <div class="caretaker-title">ℹ️ Dieto Caretaker Tip (Sahan)</div>
                <div class="caretaker-desc" id="descDiner2">
                    Your dish choice puts you above your daily budget. Don't worry! We suggest:
                </div>
                <label class="checkbox-container" style="margin-top: 6px;">
                    <input type="checkbox" id="swapDiner2" onchange="applySwapDiner2()">
                    🔄 Neutralize: Swap Dal Tadka for Tandoori Salad (-100 kcal)
                </label>
            </div>
        </div>

        <!-- Joint checkout order button -->
        <button class="btn-order" id="btnPlaceOrder" disabled onclick="checkoutJointOrder()">Place Group Swiggy Order (0 kcal)</button>

        <!-- MCP log panel -->
        <div class="terminal-panel" id="mcpTerminal">
            [MCP System] Ready to match diner preferences.
        </div>
    </div>
</div>

<script>
    // Initial states
    let baseDiner1 = 1420;
    let baseDiner2 = 1580;
    
    let targetDiner1 = 2000;
    let targetDiner2 = 2000;

    let cartDiner1 = null;
    let cartDiner2 = null;
    
    let orderPlacedId = "";

    const MENU_ITEMS = [
        { name: "Shawarma", calories: 550, protein: 24, price: 180 },
        { name: "Dal Tadka", calories: 450, protein: 18, price: 150 },
        { name: "Chicken Tikka Wrap", calories: 480, protein: 32, price: 190 },
        { name: "Paneer Rice Bowl", calories: 560, protein: 20, price: 210 },
        { name: "Lime Soda", calories: 120, protein: 0, price: 60 },
        { name: "Mint Juice", calories: 45, protein: 1, price: 80 }
    ];

    function logTerminal(msg) {
        const console = document.getElementById('mcpTerminal');
        const time = new Date().toLocaleTimeString();
        console.innerHTML += `<br>[${time}] ${msg}`;
        console.scrollTop = console.scrollHeight;
    }

    function findMatchedRestaurants() {
        const pref1 = document.getElementById('diner1Pref').value;
        const pref2 = document.getElementById('diner2Pref').value;
        
        logTerminal(`[MCP] Call: search_restaurants("query":"${pref1}") -> Intersecting...`);
        logTerminal(`[MCP] Call: search_restaurants("query":"${pref2}") -> Intersecting...`);

        setTimeout(() => {
            document.getElementById('matchedRestaurantsSection').style.display = 'flex';
            logTerminal(`[MCP] Matched 1 restaurant serving both: "Indian Spice Junction"`);
        }, 600);
    }

    function selectRestaurant(id) {
        document.getElementById('restJunctionRow').className = "restaurant-row selected";
        document.getElementById('menuSection').style.display = 'flex';
        
        const grid = document.getElementById('menuGrid');
        grid.innerHTML = '';
        
        logTerminal(`[MCP] Call: get_restaurant_menu("restaurantId":"${id}") -> Loaded 6 items`);

        MENU_ITEMS.forEach(item => {
            const card = document.createElement('div');
            card.className = 'menu-card';
            card.innerHTML = `
                <div class="menu-details">
                    <div class="menu-name">${item.name}</div>
                    <div class="menu-meta">₹${item.price} | 🔥 ${item.calories} kcal</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                    <button class="btn-add-item" onclick="addItemToDiner1('${item.name}', ${item.calories})">+ Diner 1</button>
                    <button class="btn-add-item" onclick="addItemToDiner2('${item.name}', ${item.calories})">+ Diner 2</button>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    function addItemToDiner1(name, calories) {
        cartDiner1 = { name, calories };
        logTerminal(`[MCP] Diner 1 added: update_food_cart("${name}")`);
        updateTrackers();
    }

    function addItemToDiner2(name, calories) {
        cartDiner2 = { name, calories };
        logTerminal(`[MCP] Diner 2 added: update_food_cart("${name}")`);
        updateTrackers();
    }

    function updateTrackers() {
        const mode1 = document.getElementById('modeDiner1').value;
        const mode2 = document.getElementById('modeDiner2').value;
        
        // Mode thresholds
        targetDiner1 = mode1 === 'strict' ? 1600 : (mode1 === 'balanced' ? 2000 : 2800);
        targetDiner2 = mode2 === 'strict' ? 1600 : (mode2 === 'balanced' ? 2000 : 2800);

        document.getElementById('labelDiner1').innerText = `${document.getElementById('diner1Name').value} (Diner 1)`;
        document.getElementById('labelDiner2').innerText = `${document.getElementById('diner2Name').value} (Diner 2)`;

        // Calculate diner 1 projected
        let add1 = cartDiner1 ? cartDiner1.calories : 0;
        if (document.getElementById('swapDiner1').checked && document.getElementById('tipDiner1').style.display === 'flex') {
            add1 = 420; // Swapped to Wrap
        }
        const proj1 = baseDiner1 + add1;
        const bar1 = document.getElementById('barDiner1');
        const val1 = document.getElementById('valDiner1');
        
        bar1.style.width = `${Math.min(100, (proj1 / targetDiner1) * 100)}%`;
        val1.innerText = `${proj1} / ${targetDiner1} kcal`;
        
        if (proj1 > targetDiner1) {
            bar1.classList.add('excessive');
            document.getElementById('tipDiner1').style.display = 'flex';
            document.getElementById('descDiner1').innerText = `Your choice (${cartDiner1.name}) exceeds your daily mode budget. Rather than stopping your order, we suggest neutralising:`;
        } else {
            bar1.classList.remove('excessive');
            document.getElementById('tipDiner1').style.display = 'none';
        }

        // Calculate diner 2 projected
        let add2 = cartDiner2 ? cartDiner2.calories : 0;
        if (document.getElementById('swapDiner2').checked && document.getElementById('tipDiner2').style.display === 'flex') {
            add2 = 350; // Swapped to Salad
        }
        const proj2 = baseDiner2 + add2;
        const bar2 = document.getElementById('barDiner2');
        const val2 = document.getElementById('valDiner2');

        bar2.style.width = `${Math.min(100, (proj2 / targetDiner2) * 100)}%`;
        val2.innerText = `${proj2} / ${targetDiner2} kcal`;

        if (proj2 > targetDiner2) {
            bar2.classList.add('excessive');
            document.getElementById('tipDiner2').style.display = 'flex';
            document.getElementById('descDiner2').innerText = `Your choice (${cartDiner2.name}) exceeds your daily mode budget. Rather than stopping your order, we suggest neutralising:`;
        } else {
            bar2.classList.remove('excessive');
            document.getElementById('tipDiner2').style.display = 'none';
        }

        // Enable button
        const btnOrder = document.getElementById('btnPlaceOrder');
        btnOrder.disabled = !cartDiner1 && !cartDiner2;
        const finalSumCal = add1 + add2;
        btnOrder.innerText = `Place Group Swiggy Order (${finalSumCal} kcal)`;
    }

    function applySwapDiner1() {
        updateTrackers();
    }

    function applySwapDiner2() {
        updateTrackers();
    }

    function checkoutJointOrder() {
        document.getElementById('btnPlaceOrder').disabled = true;
        logTerminal("[MCP] Initializing Swiggy MCP checkout tools...");

        setTimeout(() => {
            logTerminal("[MCP] Call: get_addresses() -> Completed (200 OK)");
            logTerminal("[MCP] Address resolved: Home (ID: addr_01HXYZ)");

            setTimeout(() => {
                logTerminal("[MCP] Call: update_food_cart() -> Completed (200 OK)");

                setTimeout(() => {
                    logTerminal("[MCP] Call: place_food_order() -> Completed (200 OK)");
                    
                    const orderId = "ord_swiggy_7711";
                    orderPlacedId = orderId;
                    logTerminal(`[MCP] Success! Order placed. ID: ${orderId}`);
                    logTerminal("[SYSTEM] Swiggy Order Completed successfully!");

                    // POST call to fastapi sync-order
                    fetch('/sync-order', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ order_id: orderId })
                    })
                    .then(r => r.json())
                    .then(data => {
                        logTerminal(`[SYSTEM] Synced Dieto group logs successfully.`);
                        
                        // Show plate scanner
                        document.getElementById('postOrderPanel').style.display = 'flex';
                        document.getElementById('comparisonBadge').innerText = "Awaiting delivery scan... 🍕";
                    });
                }, 800);
            }, 600);
        }, 800);
    }

    function triggerSimulatedScan() {
        if (!orderPlacedId) return;
        document.getElementById('comparisonBadge').innerText = "📷 Scanning camera feed... Detecting items...";
        
        setTimeout(() => {
            fetch('/compare-plate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    order_id: orderPlacedId,
                    detected_items: ["Chicken Biryani", "Chicken 65", "Raita"]
                })
            })
            .then(r => r.json())
            .then(data => {
                const badge = document.getElementById('comparisonBadge');
                badge.innerText = "Divergence found: +280 kcal";
                badge.className = "comparison-badge warn";

                const details = document.getElementById('plateScanDetails');
                details.innerHTML = `<strong>Diner Group Order Est</strong>: 1000 kcal<br>` +
                                    `<strong>Scanned Plate Actual Est</strong>: 1280 kcal<br>` +
                                    `<strong>Portion Difference</strong>: +280 kcal`;

                const adviceList = document.getElementById('wellnessAdviceList');
                adviceList.innerHTML = '<strong>Dieto AI Caretaker Aftereffects Suggestions</strong>:';
                data.coach_advice.recommendations.forEach(rec => {
                    const div = document.createElement('div');
                    div.style.margin = '4px 0';
                    div.innerText = rec;
                    adviceList.appendChild(div);
                });
            });
        }, 1200);
    }
</script>

</body>
</html>
"""
