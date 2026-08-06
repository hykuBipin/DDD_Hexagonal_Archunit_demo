HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dieto Caretaker AI Mobile App</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #FC8019; /* Swiggy Orange */
            --primary-light: #ffefe2;
            --accent-green: #10B981;
            --accent-green-light: #e6f7f0;
            --bg-outer: #0f172a;
            --bg-phone: #ffffff;
            --text-main: #1c1c1c;
            --text-muted: #686b78;
            --border-light: #f1f3f6;
            --shadow-premium: 0 25px 50px -12px rgba(0,0,0,0.5);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow: auto;
        }

        /* Premium Phone Bezel Container */
        .phone-frame {
            width: 390px;
            height: 844px;
            background-color: #000000;
            border-radius: 48px;
            padding: 12px;
            box-shadow: var(--shadow-premium), 0 0 0 4px #334155;
            position: relative;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Dynamic Island / Notch Mockup */
        .phone-island {
            width: 110px;
            height: 30px;
            background-color: #000000;
            border-radius: 15px;
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Screen Container */
        .phone-screen {
            background-color: var(--bg-phone);
            color: var(--text-main);
            width: 100%;
            height: 100%;
            border-radius: 38px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            position: relative;
            padding-top: 36px;
            scrollbar-width: none; /* Hide scrollbars */
        }

        .phone-screen::-webkit-scrollbar {
            display: none;
        }

        /* Status bar */
        .status-bar {
            padding: 8px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            font-weight: 600;
            color: #000000;
            position: absolute;
            top: 12px;
            width: 100%;
            z-index: 999;
        }

        /* Profile Header */
        .app-header {
            padding: 16px 20px 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-light);
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary), #ffb27a);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 16px;
        }

        .app-title-badge {
            background-color: var(--accent-green-light);
            color: var(--accent-green);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }

        /* Scrollable content container */
        .app-body {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            flex-grow: 1;
        }

        /* Section Title */
        .section-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
        }

        /* Profile settings card */
        .card-profile {
            background-color: #fafbfc;
            border: 1px solid var(--border-light);
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .field-group {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .field-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
        }

        .profile-select {
            padding: 8px 12px;
            border: 1px solid #dcdfe6;
            border-radius: 8px;
            font-size: 13px;
            outline: none;
            background: white;
            cursor: pointer;
        }

        .pref-checklist {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 4px;
        }

        .pref-checkbox-label {
            font-size: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            color: var(--text-main);
        }

        /* Calorie Tracker Ring/Card */
        .card-tracker {
            background-color: #ffffff;
            border: 1px solid var(--border-light);
            box-shadow: 0 4px 20px rgba(0,0,0,0.03);
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .progress-bar-container {
            background-color: #eef1f6;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            width: 100%;
        }

        .progress-bar-fill {
            background: linear-gradient(90deg, var(--accent-green), #f59e0b);
            height: 100%;
            width: 0%;
            border-radius: 5px;
            transition: width 0.3s ease;
        }

        .progress-bar-fill.excess {
            background: linear-gradient(90deg, #f59e0b, #ef4444);
        }

        /* Caretaker Tip Card */
        .caretaker-tip-card {
            background-color: var(--accent-green-light);
            border: 1px solid rgba(16, 185, 129, 0.15);
            border-radius: 16px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .caretaker-title {
            color: var(--accent-green);
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .caretaker-body {
            font-size: 12px;
            line-height: 1.4;
            color: #064e3b;
        }

        .caretaker-tips-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 4px;
        }

        .caretaker-item {
            background: white;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-main);
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            border-left: 3px solid var(--accent-green);
        }

        /* Swiggy Menu list */
        .menu-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .menu-item-row {
            background-color: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }

        .item-details {
            max-width: 70%;
        }

        .item-name {
            font-size: 13px;
            font-weight: 700;
        }

        .item-kcal {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .btn-add-item {
            border: 1px solid #dcdfe6;
            background: white;
            color: #60b246;
            font-weight: 700;
            font-size: 12px;
            padding: 6px 16px;
            border-radius: 6px;
            cursor: pointer;
        }

        .btn-add-item:hover {
            background-color: #f9f9f9;
        }

        /* Bottom Fixed Checkout bar */
        .checkout-bar {
            background-color: #ffffff;
            border-top: 1px solid var(--border-light);
            padding: 16px 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border-bottom-left-radius: 38px;
            border-bottom-right-radius: 38px;
        }

        .btn-checkout {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            box-shadow: 0 4px 15px rgba(252, 128, 25, 0.2);
            transition: transform 0.1s;
        }

        .btn-checkout:active {
            transform: scale(0.98);
        }

        /* Interactive Viewfinder Camera Overlay modal */
        .camera-overlay {
            position: absolute;
            top: 36px;
            left: 0;
            width: 100%;
            height: calc(100% - 36px);
            background-color: rgba(0,0,0,0.85);
            border-bottom-left-radius: 38px;
            border-bottom-right-radius: 38px;
            z-index: 2000;
            display: none;
            flex-direction: column;
            padding: 20px;
            color: white;
        }

        .camera-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .viewfinder {
            flex-grow: 1;
            border: 2px dashed rgba(255,255,255,0.4);
            border-radius: 16px;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0.4) 100%);
        }

        .scan-line {
            width: 100%;
            height: 2px;
            background-color: var(--accent-green);
            position: absolute;
            top: 0;
            animation: scanAnim 2.5s infinite linear;
            box-shadow: 0 0 8px var(--accent-green);
        }

        @keyframes scanAnim {
            0% { top: 0%; }
            50% { top: 100%; }
            100% { top: 0%; }
        }

        .scanned-plate-mock {
            width: 180px;
            height: 180px;
            border-radius: 90px;
            border: 4px solid white;
            background-color: #222;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.6);
        }

        /* Mock Bounding Box detections */
        .bounding-box {
            position: absolute;
            border: 2px solid #00FF66;
            background-color: rgba(0,255,102,0.1);
            color: #00FF66;
            font-size: 8px;
            font-weight: 700;
            padding: 2px;
            border-radius: 4px;
        }

        .camera-footer {
            padding: 20px 0 10px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .btn-confirm-scan {
            background-color: var(--accent-green);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            text-align: center;
        }

        /* Delivery Notification banner */
        .notification-banner {
            background-color: rgba(0,0,0,0.9);
            color: white;
            border-radius: 16px;
            padding: 12px 16px;
            display: none;
            align-items: center;
            gap: 12px;
            position: absolute;
            top: 50px;
            left: 16px;
            right: 16px;
            z-index: 1500;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .btn-scan-trigger {
            background-color: var(--accent-green);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div class="phone-frame">
    <!-- Notch / Dynamic Island -->
    <div class="phone-island"></div>

    <div class="phone-screen">
        <!-- Status Bar -->
        <div class="status-bar">
            <span>09:41</span>
            <div style="display:flex; gap:4px;">📶 🔋</div>
        </div>

        <!-- Notification Banner -->
        <div class="notification-banner" id="deliveryNotification">
            <span style="font-size: 20px;">🛵</span>
            <div style="flex-grow: 1;">
                <div style="font-size: 11px; font-weight: 700;">SWIGGY DELIVERY</div>
                <div style="font-size: 10px; opacity: 0.85;">Your order has arrived!</div>
            </div>
            <button class="btn-scan-trigger" onclick="openCameraView()">Camera Scan</button>
        </div>

        <!-- Camera Overlay Mock -->
        <div class="camera-overlay" id="cameraOverlay">
            <div class="camera-header">
                <span style="font-weight: 700; font-size: 14px;">Plate scanner AI</span>
                <span style="cursor: pointer; font-size: 18px;" onclick="closeCameraView()">✕</span>
            </div>
            <div class="viewfinder">
                <div class="scan-line"></div>
                <div class="scanned-plate-mock">🍽️</div>
                <!-- green bounding boxes -->
                <div class="bounding-box" style="top: 25%; left: 20%; width: 90px; height: 50px;">Chicken Biryani (650 kcal)</div>
                <div class="bounding-box" style="top: 45%; left: 55%; width: 75px; height: 40px;">Chicken 65 (450 kcal)</div>
                <div class="bounding-box" style="top: 60%; left: 25%; width: 60px; height: 35px;">Raita (80 kcal)</div>
            </div>
            <div class="camera-footer">
                <p style="font-size: 11px; text-align: center; opacity: 0.8;">Detecting portion sizes to verify total intake</p>
                <button class="btn-confirm-scan" onclick="confirmPlateScan()">Confirm Scanned Plate</button>
            </div>
        </div>

        <!-- Header -->
        <div class="app-header">
            <div class="user-profile">
                <div class="avatar" id="avatarLetter">B</div>
                <div>
                    <div style="font-weight: 700; font-size: 14px;" id="profileName">Bipin</div>
                    <div style="font-size: 10px; color: var(--text-muted);">Indiranagar, Bangalore</div>
                </div>
            </div>
            <span class="app-title-badge">Caretaker AI</span>
        </div>

        <!-- Body -->
        <div class="app-body">
            <!-- Calorie Tracker Box -->
            <div class="card-tracker">
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700;">
                    <span>Daily Calorie Tracker</span>
                    <span id="trackerNums">1,200 / 2,000 kcal</span>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" id="progressBarFill"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-muted);">
                    <span id="txtRemaining">Remaining: 800 kcal</span>
                    <span id="txtActiveMode" style="font-weight:600;">Balanced Mode</span>
                </div>
            </div>

            <!-- Profile and Restrictions Settings -->
            <div class="card-profile">
                <div class="field-group">
                    <span class="field-label">Target Mode</span>
                    <select id="dietModeSelect" class="profile-select" onchange="updateTrackers()">
                        <option value="strict">Strict Mode (1,600 kcal limit)</option>
                        <option value="balanced" selected>Balanced Mode (2,000 kcal limit)</option>
                        <option value="relaxed">Relaxed Mode (2,800 kcal limit)</option>
                    </select>
                </div>
                <div class="field-group">
                    <span class="field-label">Dietary Guidelines</span>
                    <div class="pref-checklist">
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

            <!-- Encouraging Caretaker Suggestions Advice Card -->
            <div class="caretaker-tip-card" id="caretakerCard">
                <div class="caretaker-title">🌟 Dieto Caretaker Tip</div>
                <div class="caretaker-body" id="caretakerIntro">
                    Food is joy and fuel! We encourage you to enjoy your meal. Here are encouraging wellness tips based on your menu selection and profile preferences:
                </div>
                <div class="caretaker-tips-list" id="tipsContainer">
                    <!-- Dynamic tips populated here -->
                </div>
            </div>

            <!-- Swiggy Menu Grid list -->
            <div>
                <span class="section-title">Swiggy Integrated Menu</span>
                <div class="menu-list" style="margin-top:10px;" id="menuList">
                    <!-- Menu items list loaded dynamically -->
                </div>
            </div>

            <!-- Post-scan verification details -->
            <div class="card-tracker" id="plateVerificationCard" style="display:none; border-left:4px solid var(--accent-green);">
                <div style="font-weight: 700; font-size: 13px; color: var(--accent-green);">🍽️ Scanned Plate Verification</div>
                <div id="plateScanSummary" style="font-size:12px; margin-top:6px; line-height:1.5;"></div>
                <div id="scannedCoachAdviceList" style="display:flex; flex-direction:column; gap:6px; margin-top:8px;"></div>
            </div>
        </div>

        <!-- Checkout Fixed Bottom bar -->
        <div class="checkout-bar">
            <button class="btn-checkout" id="btnPlaceOrder" onclick="placeOrder()">Place Swiggy Order (0 kcal)</button>
        </div>
    </div>
</div>

<script>
    let baseCalories = 1200;
    let targetCalories = 2000;
    let selectedItem = null;
    let orderPlacedId = "";

    const MENU_ITEMS = [
        { name: "Double Cheese Burger", calories: 680, price: 240 },
        { name: "Paneer Rice Bowl", calories: 560, price: 210 },
        { name: "Chicken Tikka Wrap", calories: 480, price: 180 },
        { name: "Tandoori Chicken Salad", calories: 350, price: 220 },
        { name: "Lime Soda", calories: 120, price: 60 },
        { name: "Mint Juice", calories: 45, price: 80 }
    ];

    function loadMenu() {
        const list = document.getElementById('menuList');
        list.innerHTML = '';
        MENU_ITEMS.forEach(item => {
            const row = document.createElement('div');
            row.className = 'menu-item-row';
            row.innerHTML = `
                <div class="item-details">
                    <div class="item-name">${item.name}</div>
                    <div class="item-kcal">🔥 ${item.calories} kcal | ₹${item.price}</div>
                </div>
                <button class="btn-add-item" onclick="addItem('${item.name}', ${item.calories})">+ ADD</button>
            `;
            list.appendChild(row);
        });
    }

    function addItem(name, calories) {
        selectedItem = { name, calories };
        updateTrackers();
    }

    function updateTrackers() {
        const mode = document.getElementById('dietModeSelect').value;
        targetCalories = mode === 'strict' ? 1600 : (mode === 'balanced' ? 2000 : 2800);
        
        document.getElementById('txtActiveMode').innerText = mode.charAt(0).toUpperCase() + mode.slice(1) + " Mode";

        const added = selectedItem ? selectedItem.calories : 0;
        const projected = baseCalories + added;
        
        // Progress Fill
        const bar = document.getElementById('progressBarFill');
        const percent = Math.min(100, (projected / targetCalories) * 100);
        bar.style.width = `${percent}%`;
        if (projected > targetCalories) {
            bar.classList.add('excess');
        } else {
            bar.classList.remove('excess');
        }

        document.getElementById('trackerNums').innerText = `${projected} / ${targetCalories} kcal`;
        const remaining = targetCalories - projected;
        document.getElementById('txtRemaining').innerText = remaining >= 0 ? `Remaining: ${remaining} kcal` : `Over Budget by: ${Math.abs(remaining)} kcal`;

        // Update checkout button text
        document.getElementById('btnPlaceOrder').innerText = `Place Swiggy Order (${added} kcal)`;

        // Fetch Dynamic Wellness Suggestions from API
        const noSugar = document.getElementById('chkNoSugar').checked;
        const noGarlic = document.getElementById('chkNoGarlic').checked;
        const glutenFree = document.getElementById('chkGlutenFree').checked;

        const excess = projected > targetCalories ? (projected - targetCalories) : 0;
        const itemsList = selectedItem ? [selectedItem.name] : [];

        fetch('/recovery', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                excess_calories: excess,
                no_sugar: noSugar,
                no_garlic: noGarlic,
                gluten_free: glutenFree,
                cart_items: itemsList
            })
        })
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById('tipsContainer');
            container.innerHTML = '';
            
            data.recommendations.forEach(rec => {
                const item = document.createElement('div');
                item.className = 'caretaker-item';
                item.innerText = rec;
                container.appendChild(item);
            });
        });
    }

    function placeOrder() {
        if (!selectedItem) return;
        document.getElementById('btnPlaceOrder').disabled = true;

        setTimeout(() => {
            const orderId = "ord_swiggy_7711";
            orderPlacedId = orderId;
            
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
                
                // Show Swiggy delivery push notification
                document.getElementById('deliveryNotification').style.display = 'flex';
                document.getElementById('btnPlaceOrder').disabled = false;
            });
        }, 1200);
    }

    function openCameraView() {
        document.getElementById('deliveryNotification').style.display = 'none';
        document.getElementById('cameraOverlay').style.display = 'flex';
    }

    function closeCameraView() {
        document.getElementById('cameraOverlay').style.display = 'none';
    }

    function confirmPlateScan() {
        document.getElementById('cameraOverlay').style.display = 'none';

        const noSugar = document.getElementById('chkNoSugar').checked;
        const noGarlic = document.getElementById('chkNoGarlic').checked;
        const glutenFree = document.getElementById('chkGlutenFree').checked;

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
            const card = document.getElementById('plateVerificationCard');
            card.style.display = 'flex';

            const summary = document.getElementById('plateScanSummary');
            summary.innerHTML = `<strong>Divergence detected</strong>: +280 kcal portion excess.<br>` +
                                `Enjoy the extra bites! Here is how we balance comfortably:`;

            const list = document.getElementById('scannedCoachAdviceList');
            list.innerHTML = '';
            data.coach_advice.recommendations.forEach(rec => {
                const item = document.createElement('div');
                item.className = 'caretaker-item';
                item.innerText = rec;
                list.appendChild(item);
            });
        });
    }

    window.onload = () => {
        loadMenu();
        updateTrackers();
    }
</script>

</body>
</html>
"""
