# 🛍️ Shopping Behavior Analytics Dashboard

A beautiful, interactive web dashboard for analyzing shopping behavior using Machine Learning and Flask.

## ✨ Features

- **📊 Real-time Dashboard** - Overview statistics with beautiful visualizations
- **📈 Interactive Charts** - Category analysis, seasonal trends, age distribution, and more
- **🎯 ML-Powered Predictor** - Predict purchase amounts and subscription probability
- **💡 Smart Insights** - Automated insights based on customer data
- **📱 Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **🎨 Modern UI** - Beautiful gradients, animations, and smooth transitions

## 🚀 Quick Start

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

Navigate to: **http://127.0.0.1:5000**

## 📁 Project Structure

```
Shopping Behav/
├── app.py                              # Flask backend
├── templates/
│   └── index.html                      # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css                   # Styles
│   └── js/
│       └── main.js                     # JavaScript logic
├── shopping_behavior_updated.csv       # Dataset
├── shopping_behavior_eda.ipynb         # Analysis notebook
└── requirements.txt                    # Dependencies
```

## 🎯 Dashboard Sections

### 1. Overview
- Total customers
- Total revenue
- Average purchase amount
- Average rating
- Subscription rate
- Discount usage

### 2. Analytics
- Purchase by category
- Seasonal trends
- Age distribution
- Payment methods
- Top selling items
- Customer segments

### 3. Predictor
Enter customer information to predict:
- Purchase amount
- Subscription probability

### 4. Insights
- Customer demographics
- Revenue insights
- Marketing opportunities
- Customer satisfaction
- Recent transactions

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **ML:** scikit-learn, pandas, numpy
- **Design:** Modern gradients, animations, responsive layout

## 📊 Machine Learning Models

1. **Random Forest Regressor** - Purchase amount prediction
2. **Random Forest Classifier** - Subscription prediction
3. **K-Means Clustering** - Customer segmentation

## 🎨 Design Features

- Modern gradient backgrounds
- Smooth animations and transitions
- Interactive charts with hover effects
- Glassmorphism effects
- Responsive grid layouts
- Beautiful color palette

## 📝 API Endpoints

- `GET /` - Main dashboard
- `GET /api/overview` - Overview statistics
- `GET /api/purchase_by_category` - Category analysis
- `GET /api/seasonal_trends` - Seasonal trends
- `GET /api/age_distribution` - Age distribution
- `GET /api/top_items` - Top selling items
- `GET /api/cluster_data` - Customer segments
- `GET /api/payment_methods` - Payment method distribution
- `GET /api/recent_transactions` - Recent transaction data
- `POST /api/predict` - Make predictions

## 💡 Usage Tips

1. **Explore the Dashboard** - Scroll through different sections
2. **Interact with Charts** - Hover over data points for details
3. **Try the Predictor** - Enter customer details to get predictions
4. **Check Insights** - Review automated insights and recommendations

## 🔧 Customization

### Change Colors
Edit `static/css/style.css` - `:root` variables:
```css
--primary: #6366f1;
--secondary: #ec4899;
--success: #10b981;
```

### Add More Charts
1. Add endpoint in `app.py`
2. Add chart canvas in `templates/index.html`
3. Add chart function in `static/js/main.js`

## 📈 Performance

- Fast load times with optimized assets
- Efficient data processing with pandas
- Cached model predictions
- Responsive charts with Chart.js

## 🤝 Contributing

Feel free to fork, modify, and enhance this dashboard!

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ using Flask, Machine Learning, and Modern Web Technologies**
