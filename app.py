"""
NestFinder Pakistan: Rental Homes
A Streamlit app for browsing and booking rental properties across Pakistan.
"""
import streamlit as st
import json
import os
from pathlib import Path
from datetime import date, timedelta, datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NestFinder Pakistan",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Paths (relative, deploy-safe) ─────────────────────────────────────────────
APP_DIR = Path(__file__).parent
PROPERTIES_FILE = APP_DIR / "properties.json"
BOOKINGS_FILE = APP_DIR / "bookings.json"

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1a1a2e;
    color: #e0d9c8;
}
section[data-testid="stSidebar"] * { color: #e0d9c8 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stNumberInput > div > div > input,
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: #16213e !important;
    border: 1px solid #c8a96e !important;
    color: #e0d9c8 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stSlider > div { color: #c8a96e !important; }
section[data-testid="stSidebar"] label { color: #c8a96e !important; font-weight: 500; }

/* Main area */
.main { background: #f7f3ee; }
.block-container { padding-top: 2rem !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(200,169,110,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    color: #e0d9c8;
    margin: 0 0 0.5rem;
}
.hero p { color: #a09078; font-size: 1.15rem; margin: 0; }
.hero .accent { color: #c8a96e; }

/* Property cards */
.prop-card {
    background: #ffffff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    margin-bottom: 1.5rem;
    border: 1px solid #ece8e1;
    height: 100%;
}
.prop-card:hover { transform: translateY(-4px); box-shadow: 0 10px 32px rgba(0,0,0,0.13); }

.prop-img-wrap {
    width: 100%; height: 200px; position: relative; overflow: hidden;
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
}
.prop-img-wrap img {
    width: 100%; height: 100%; object-fit: cover;
}
.prop-img-emoji {
    position: absolute; top: 10px; left: 10px;
    background: rgba(26, 26, 46, 0.85);
    color: #c8a96e;
    padding: 4px 10px; border-radius: 20px;
    font-size: 1.1rem;
}
.prop-img-price {
    position: absolute; bottom: 10px; right: 10px;
    background: rgba(26, 26, 46, 0.9);
    color: #c8a96e;
    padding: 5px 12px; border-radius: 20px;
    font-size: 0.85rem; font-weight: 600;
}
.prop-body { padding: 1.25rem 1.4rem 1.4rem; }
.prop-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem; color: #1a1a2e; font-weight: 600; margin: 0 0 0.35rem;
}
.prop-loc { color: #907060; font-size: 0.88rem; margin: 0 0 0.75rem; }
.prop-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.85rem; }
.tag {
    background: #f0ece5; color: #5a4a3a; font-size: 0.75rem;
    padding: 3px 10px; border-radius: 20px; font-weight: 500;
}
.prop-price { color: #c8a96e; font-size: 1.3rem; font-weight: 700; }
.prop-price span { color: #9a8a7a; font-size: 0.82rem; font-weight: 400; }
.prop-meta { color: #5a4a3a; font-size: 0.88rem; }

/* Booking form */
.booking-box {
    background: #1a1a2e;
    border-radius: 16px;
    padding: 2rem;
    color: #e0d9c8;
}
.booking-box h3 {
    font-family: 'Playfair Display', serif;
    color: #c8a96e;
    margin-top: 0;
}

/* Section headings */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem; color: #1a1a2e;
    border-left: 4px solid #c8a96e;
    padding-left: 0.75rem;
    margin: 2rem 0 1.25rem;
}

/* Confirmation box */
.confirm-box {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    border-radius: 16px; padding: 2rem;
    border: 1px solid #c8a96e; margin-top: 1rem;
}
.confirm-box h2 { font-family:'Playfair Display',serif; color:#c8a96e; }
.confirm-box p  { color:#e0d9c8; line-height:1.8; }

/* Divider */
hr.gold { border: none; border-top: 1px solid #c8a96e33; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_properties():
    """Load property catalogue from JSON. Cached for performance."""
    with open(PROPERTIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_bookings():
    """Load bookings from disk. Returns [] if file missing or unreadable."""
    if BOOKINGS_FILE.exists():
        try:
            with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_bookings(bookings):
    """Persist bookings to disk. Silently no-ops if filesystem is read-only
    (the app still works via session_state in that case)."""
    try:
        with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(bookings, f, indent=2, ensure_ascii=False)
    except OSError:
        pass


def is_booked(prop_id, check_in, check_out, bookings):
    """Return True if this property has overlapping booking on the given dates."""
    for b in bookings:
        if b["property_id"] == prop_id:
            bi = date.fromisoformat(b["check_in"])
            bo = date.fromisoformat(b["check_out"])
            if not (check_out <= bi or check_in >= bo):
                return True
    return False


PROPERTIES = load_properties()

# ── Session state ─────────────────────────────────────────────────────────────
if "bookings" not in st.session_state:
    st.session_state.bookings = load_bookings()
if "selected_prop" not in st.session_state:
    st.session_state.selected_prop = None
if "last_booking" not in st.session_state:
    st.session_state.last_booking = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏡 NestFinder")
    st.markdown("Pakistan's curated rental homes platform.")
    st.markdown("---")
    nav = st.radio(
        "Navigate",
        ["Browse Homes", "My Bookings", "About"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### 🔍 Filters")

    cities = ["All"] + sorted({p["city"] for p in PROPERTIES})
    fcity = st.selectbox("City", cities)

    prop_types = ["All"] + sorted({p["type"] for p in PROPERTIES})
    ftype = st.selectbox("Property Type", prop_types)

    fguests = st.number_input("Min. Guests", 1, 20, 1)
    fmax_price = st.slider("Max Price / Night (PKR)", 3000, 35000, 35000, step=500)

    keyword = st.text_input("Search (name, area, amenity)", placeholder="e.g. pool, Hunza, villa")

    st.markdown("---")
    st.markdown(
        "<small style='color:#9a8a7a'>© 2026 NestFinder Pakistan</small>",
        unsafe_allow_html=True,
    )


# ── Helper: Filter properties ─────────────────────────────────────────────────
def filter_properties():
    out = []
    kw = keyword.lower().strip()
    for p in PROPERTIES:
        if fcity != "All" and p["city"] != fcity:
            continue
        if ftype != "All" and p["type"] != ftype:
            continue
        if p["guests"] < fguests:
            continue
        if p["price"] > fmax_price:
            continue
        if kw:
            hay = (
                p["name"].lower()
                + " " + p["location"].lower()
                + " " + p["type"].lower()
                + " " + " ".join(a.lower() for a in p["amenities"])
                + " " + p["description"].lower()
            )
            if kw not in hay:
                continue
        out.append(p)
    return out


# ── Pages ─────────────────────────────────────────────────────────────────────

# ─── BROWSE ───────────────────────────────────────────────────────────────────
if nav == "Browse Homes":

    st.markdown("""
    <div class="hero">
        <h1>Find Your <span class="accent">Perfect</span> Rental Home</h1>
        <p>Handpicked properties across Pakistan, from mountain retreats to city penthouses.</p>
    </div>
    """, unsafe_allow_html=True)

    filtered = filter_properties()

    if not filtered:
        st.warning("No properties match your filters. Try adjusting them.")
    else:
        st.markdown(
            f'<div class="section-title">Available Properties '
            f'<span style="font-size:1rem;color:#9a8a7a;font-family:DM Sans">'
            f'({len(filtered)} found)</span></div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for i, prop in enumerate(filtered):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="prop-card">
                    <div class="prop-img-wrap">
                        <img src="{prop['image']}" alt="{prop['name']}" loading="lazy" />
                        <div class="prop-img-emoji">{prop['emoji']} {prop['type']}</div>
                        <div class="prop-img-price">PKR {prop['price']:,} / night</div>
                    </div>
                    <div class="prop-body">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
                            <div class="prop-title">{prop['name']}</div>
                            <div>⭐ {prop['rating']}</div>
                        </div>
                        <div class="prop-loc">📍 {prop['location']}</div>
                        <div class="prop-tags">
                            {''.join(f'<span class="tag">{a}</span>' for a in prop['amenities'][:4])}
                        </div>
                        <div class="prop-meta">
                            🛏 {prop['bedrooms']} bed · 🚿 {prop['bathrooms']} bath · 👥 {prop['guests']} guests
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Book Now", key=f"book_{prop['id']}", use_container_width=True):
                    st.session_state.selected_prop = prop
                    st.session_state.last_booking = None
                    st.rerun()

    # ── Booking section ──────────────────────────────────────────────────────
    if st.session_state.selected_prop:
        prop = st.session_state.selected_prop
        st.markdown('<hr class="gold">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="section-title">{prop["emoji"]} Book: {prop["name"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="color:#5a4a3a;font-size:1.05rem">{prop["description"]}</p>',
            unsafe_allow_html=True,
        )
        st.image(prop["image"], use_container_width=True)

        col_f, col_s = st.columns([1.2, 1])

        # Capture dates outside the form so the price summary on the right reacts to them
        today = date.today()
        ci_key = f"ci_{prop['id']}"
        co_key = f"co_{prop['id']}"

        with col_f:
            st.markdown("#### 📅 Stay Dates")
            d1, d2 = st.columns(2)
            ci = d1.date_input(
                "Check-in",
                value=st.session_state.get(ci_key, today + timedelta(days=1)),
                min_value=today,
                key=ci_key,
            )
            co = d2.date_input(
                "Check-out",
                value=st.session_state.get(co_key, today + timedelta(days=4)),
                min_value=today + timedelta(days=1),
                key=co_key,
            )

            with st.form("booking_form", clear_on_submit=False):
                st.markdown("#### 👤 Your Details")
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                phone = st.text_input("Phone Number")
                guests_count = st.number_input(
                    "Number of Guests", 1, prop["guests"], 1,
                    help=f"This property hosts up to {prop['guests']} guests."
                )
                st.markdown("#### 💳 Payment")
                pay_method = st.selectbox(
                    "Payment Method",
                    ["Easypaisa", "JazzCash", "Bank Transfer", "Credit / Debit Card", "Cash on Arrival"],
                )
                submitted = st.form_submit_button("✅ Confirm Booking", use_container_width=True)

            if submitted:
                if not name or not email or not phone:
                    st.error("Please fill in all your details.")
                elif "@" not in email or "." not in email:
                    st.error("Please enter a valid email address.")
                elif ci >= co:
                    st.error("Check-out must be after check-in.")
                elif is_booked(prop["id"], ci, co, st.session_state.bookings):
                    st.error("This property is already booked for those dates. Please choose different ones.")
                else:
                    nights = (co - ci).days
                    total = nights * prop["price"]
                    ref = f"NF-{prop['id']}{datetime.now().strftime('%d%m%H%M%S')}"
                    new_b = {
                        "ref": ref,
                        "property_id": prop["id"],
                        "property_name": prop["name"],
                        "location": prop["location"],
                        "emoji": prop["emoji"],
                        "image": prop["image"],
                        "name": name, "email": email, "phone": phone,
                        "guests_count": int(guests_count),
                        "check_in": ci.isoformat(), "check_out": co.isoformat(),
                        "nights": nights, "total": total,
                        "payment": pay_method,
                        "booked_on": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    }
                    st.session_state.bookings.append(new_b)
                    save_bookings(st.session_state.bookings)
                    st.session_state.last_booking = new_b
                    st.session_state.selected_prop = None
                    st.rerun()

        with col_s:
            nights_live = max(0, (co - ci).days)
            total_live = nights_live * prop["price"]
            amenities_html = "  ·  ".join(prop["amenities"])
            st.markdown(f"""
            <div class="booking-box">
                <h3>Price Summary</h3>
                <p>🏠 <b>{prop['name']}</b><br>
                📍 {prop['location']}<br>
                🛏 {prop['bedrooms']} bed · 🚿 {prop['bathrooms']} bath · 👥 up to {prop['guests']} guests</p>
                <hr style="border-color:#c8a96e44">
                <p>PKR {prop['price']:,} × {nights_live} night(s)</p>
                <p style="font-size:1.8rem;color:#c8a96e;font-weight:700">
                    PKR {total_live:,}
                </p>
                <p style="color:#a09078;font-size:0.9rem">Includes booking confirmation and 24/7 host support.</p>
                <hr style="border-color:#c8a96e44">
                <p style="color:#a09078;font-size:0.85rem"><b>Amenities</b><br>{amenities_html}</p>
                <p style="color:#a09078;font-size:0.85rem"><b>Host:</b> {prop.get('host', 'Verified Host')}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("← Back to listings"):
            st.session_state.selected_prop = None
            st.rerun()

    # ── Confirmation banner ──────────────────────────────────────────────────
    if st.session_state.last_booking:
        b = st.session_state.last_booking
        st.markdown(f"""
        <div class="confirm-box">
            <h2>🎉 Booking Confirmed!</h2>
            <p>
            <b>Reference:</b> {b['ref']}<br>
            <b>Property:</b> {b['emoji']} {b['property_name']} ({b['location']})<br>
            <b>Guest:</b> {b['name']} &nbsp;|&nbsp; 📧 {b['email']} &nbsp;|&nbsp; 📞 {b['phone']}<br>
            <b>Check-in:</b> {b['check_in']} &nbsp;→&nbsp; <b>Check-out:</b> {b['check_out']} &nbsp;({b['nights']} nights, {b['guests_count']} guest/s)<br>
            <b>Total:</b> PKR {b['total']:,} &nbsp;|&nbsp; <b>Payment:</b> {b['payment']}<br>
            <b>Booked on:</b> {b['booked_on']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Clear confirmation"):
            st.session_state.last_booking = None
            st.rerun()

# ─── MY BOOKINGS ──────────────────────────────────────────────────────────────
elif nav == "My Bookings":
    st.markdown('<div class="section-title">📋 All Bookings</div>', unsafe_allow_html=True)

    bookings = st.session_state.bookings
    if not bookings:
        st.info("No bookings yet. Browse properties and make your first booking!")
    else:
        search = st.text_input("🔍 Search by name, ref, or property", placeholder="e.g. Ahmed or NF-1234")
        shown = [
            b for b in bookings
            if not search
            or search.lower() in b["name"].lower()
            or search.lower() in b["ref"].lower()
            or search.lower() in b["property_name"].lower()
        ]

        # Quick stats
        total_revenue = sum(b["total"] for b in bookings)
        upcoming = sum(
            1 for b in bookings
            if date.fromisoformat(b["check_in"]) >= date.today()
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Bookings", len(bookings))
        c2.metric("Upcoming", upcoming)
        c3.metric("Total Revenue", f"PKR {total_revenue:,}")

        st.markdown(f"**{len(shown)}** booking(s) match your search")
        for b in reversed(shown):
            today = date.today()
            status = "🟢 Upcoming" if date.fromisoformat(b["check_in"]) >= today else "✅ Completed"
            with st.expander(
                f"{b['emoji']}  {b['property_name']}  ·  {b['name']}  ·  {b['ref']}  ·  {status}"
            ):
                c1, c2 = st.columns(2)
                c1.markdown(f"""
                **📌 Reference:** `{b['ref']}`  
                **🏠 Property:** {b['property_name']}  
                **📍 Location:** {b['location']}  
                **👤 Guest:** {b['name']}  
                **📧 Email:** {b['email']}  
                **📞 Phone:** {b['phone']}  
                **👥 Guests:** {b.get('guests_count', '-')}  
                """)
                c2.markdown(f"""
                **📅 Check-in:** {b['check_in']}  
                **📅 Check-out:** {b['check_out']}  
                **🌙 Nights:** {b['nights']}  
                **💰 Total:** PKR {b['total']:,}  
                **💳 Payment:** {b['payment']}  
                **🕐 Booked on:** {b['booked_on']}  
                """)
                if st.button("❌ Cancel Booking", key=f"cancel_{b['ref']}"):
                    st.session_state.bookings = [
                        x for x in st.session_state.bookings if x["ref"] != b["ref"]
                    ]
                    save_bookings(st.session_state.bookings)
                    st.success("Booking cancelled.")
                    st.rerun()

# ─── ABOUT ────────────────────────────────────────────────────────────────────
elif nav == "About":
    st.markdown("""
    <div class="hero">
        <h1><span class="accent">NestFinder</span> Pakistan</h1>
        <p>Your trusted platform for hassle-free rental home bookings across Pakistan.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏠 Properties", len(PROPERTIES))
    col2.metric("📋 Bookings", len(st.session_state.bookings))
    col3.metric("🌍 Cities", len({p["city"] for p in PROPERTIES}))
    col4.metric("🏷️ Property Types", len({p["type"] for p in PROPERTIES}))

    st.markdown("""
    <hr class="gold">
    <h3 style="font-family:'Playfair Display',serif;color:#1a1a2e">How It Works</h3>
    <ol style="line-height:2.2;color:#5a4a3a">
        <li><b>Browse</b>: Filter properties by city, type, guests, budget, or keyword.</li>
        <li><b>Select</b>: Click <em>Book Now</em> on any listing you love.</li>
        <li><b>Fill Details</b>: Enter your name, contact, and stay dates.</li>
        <li><b>Confirm</b>: Receive an instant booking reference.</li>
        <li><b>Manage</b>: View or cancel bookings anytime from <em>My Bookings</em>.</li>
    </ol>
    <hr class="gold">
    """, unsafe_allow_html=True)

    st.markdown("### 📍 Cities We Cover")
    city_counts = {}
    for p in PROPERTIES:
        city_counts[p["city"]] = city_counts.get(p["city"], 0) + 1
    city_str = "  ·  ".join(f"**{c}** ({n})" for c, n in sorted(city_counts.items()))
    st.markdown(city_str)

    st.markdown("""
    <hr class="gold">
    <p style="color:#9a8a7a;font-size:0.9rem">
    Built with Streamlit. Listings shown are a curated demo dataset using real Pakistan neighbourhoods.
    For commercial use, integrate with a live property data provider.
    </p>
    """, unsafe_allow_html=True)
