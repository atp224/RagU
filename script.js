const menuData = [
    { name: 'Fried Calamari', price: '$15.00', description: 'Bloody Mary ketchup sauce' },
    { name: '3 Meatballs', price: '$14.00', description: 'Pork and beef, Parmesan, parsley, basil marinara and crostini.' },
    { name: 'Mac and Cheese', price: '$14.00', description: 'with roasted bred crumb' },
    { name: '5 Dolma', price: '$9.00', description: 'Tender vine leaves rolled with rice, onion, fresh herbs and lemon olive oil.' },
    { name: 'Chicken Wings', price: '$16.00', description: 'Ranch Dressing' },
    { name: 'Mozzarella Caprese', price: '$12.00', description: 'Fresh Mozzarella cheese, fresh tomato, basil, balsamic vinaigrette, olive oil' },
    { name: 'Hummus', price: '$9.00', description: 'Pureed garbanzo beans, garlic, olive oil, lemon, tahini, pita bread' },
    { name: 'Bruschetta', price: '$9.00', description: 'Crostini, diced tomato, garlic, basil, white balsamic, parmesan cheese' },
    { name: 'Spring Mix Salad', price: '$11.00', description: 'Olives, tomato, onion, dried figs, Parmesan cheese, balsamic vinaigrette.' },
    { name: 'Caesar Salad', price: '$11.00', description: 'Romaine lettuce, Parmesan cheese, croutons and Caesar dressing.' },
    { name: 'Margherita Pizza', price: '$18.00', description: 'Tomato sauce, mozzarella cheese, fresh tomato and basil.' },
    { name: 'Sausage & Pepperoni Pizza', price: '$21.00', description: 'Tomato sauce, Mozzarella and Parmesan cheese.' },
    { name: 'Mushroom Pizza', price: '$21.00', description: 'Tomato sauce, seasonal mushrooms, arugula, mozzarella cheese, white truffle oil.' },
    { name: 'Prosciutto Pizza', price: '$21.00', description: 'Tomato sauce, caramelized onion, arugula, mozzarella and parmesan cheese.' },
    { name: 'Spaghetti Meatballs', price: '$21.00', description: 'Beef, pork, garlic and basil marinara sauce.' },
    { name: 'Penne and Chicken', price: '$21.00', description: 'Tender chicken, seasonal mushroom, spinach, sun dried tomatoes and cream sauce.' },
    { name: 'Spinach Ravioli', price: '$20.00', description: 'Ricotta cheese, fresh tomato, feta cheese, garlic, basil and marinara sauce.' },
    { name: 'Potato Gnocchi', price: '$19.00', description: 'Parmesan & gorgonzola cheese in cream sauce' },
    { name: 'Seafood Linguine', price: '$29.00', description: 'Mussels, prawns, salmon, calamari, garlic white wine marinara sauce' },
    { name: 'Flat Iron Steak', price: '$37.00', description: 'Green peppercorn oregano butter sauce, french fries and vegetables' },
    { name: 'Atlantic Salmon', price: '$27.00', description: 'Grilled salmon, sorrel, oven dried tomato, olive oil, jasmine rice and vegetables.' },
    { name: 'Chicken Shissh Kebab', price: '$23.00', description: 'Marinated chicken skewer, jasmine rice and vegetables.' },
    { name: '8 oz. Cheese Burger', price: '$18.00', description: 'Homemade bread roll, beef patty, lettuce, tomato, onion, cheddar cheese, house aioli and french fries.' },
    { name: '8 oz. Lamb and Beef Burger', price: '$19.00', description: 'Homemade bread roll, lamb and beef, chili flakes, red onion, spinach, feta cheese, house aioli and french fries.' },
    { name: 'Soma Burger', price: '$19.00', description: 'Homemade bread, pepperoni, caramelized onion, lettuce, tomato, cheddar cheese, house aioli, french fries' },
    { name: 'Chicken Sandwich', price: '$18.00', description: 'Grilled chicken, lettuce, tomato, onion, house aioli, french fries' }
];

document.addEventListener('DOMContentLoaded', (event) => {
    initializeMenuGrid();
});

// Function to initialize and render the Grid.js table
function initializeMenuGrid() {
    new gridjs.Grid({
        columns: ['Name', 'Price', 'Description'],
        data: menuData.map(item => [item.name, item.price, item.description]),
        search: true,
        sort: true,
        pagination: {
            limit: 10
        }
    }).render(document.getElementById('menu-grid'));
}

document.getElementById('promptForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Show loading symbol
    document.getElementById('loading').style.display = 'block';

    var prompt = document.getElementById('userPrompt').value;

    fetch('http://127.0.0.1:5000/save_prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading symbol
        document.getElementById('loading').style.display = 'none';

        // Display the response from the GPT-3.5-turbo API
        const apiResponseDiv = document.getElementById('apiResponse');
        apiResponseDiv.textContent = data.gpt_response;
        
        // Now show the div and add the box-shadow and border
        apiResponseDiv.style.display = 'block'; // Or 'flex' if you're using a flex layout
        apiResponseDiv.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
        apiResponseDiv.style.border = '1px solid #ddd';
    })
    .catch(error => {
        // Hide loading symbol in case of error as well
        document.getElementById('loading').style.display = 'none';
        console.error('Error:', error);
    });
});

