document.addEventListener('DOMContentLoaded', function () {
    console.log("Inside the Function")
    // Ensure that the form and checkbox exist before adding the event listener
    const addStockForm = document.getElementById('addStockForm');
    const yahooFinanceToggle = document.getElementById('yahooFinance');
    console.log(addStockForm)
    if (addStockForm && yahooFinanceToggle) {

        addStockForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission
            let isValid = true; // Flag to track if the form is valid

            // Get form fields
            const stockCode = document.getElementById('stockDropdown');
            const buyPrice = document.querySelector('input[name="buy_price"]');
            const noOfShares = document.querySelector('input[name="no_of_shares"]');
            const stopLoss = document.querySelector('input[name="stop_loss"]');
            const cashOut = document.querySelector('input[name="cash_out"]');
            const comment = document.querySelector('input[name="comment"]');
            // Clear previous error messages
            clearErrorMessages();
        
            // Validate each field using a switch statement
            [stockCode, buyPrice, noOfShares, stopLoss, cashOut,comment].forEach((input) => {
                switch (input.name) {
                    case 'stock_code':
                        if (input.value === '') {
                            showError(input, 'Please select a stock ticker.');
                            isValid = false;
                        }
                        break;
                    case 'buy_price':
                        if (input.value === '' || isNaN(input.value) || input.value <= 0) {
                            showError(input, 'Please enter a valid buy price.');
                            isValid = false;
                        }
                        break;
                    case 'no_of_shares':
                        if (input.value === '' || isNaN(input.value) || input.value <= 0) {
                            showError(input, 'Please enter a valid volume.');
                            isValid = false;
                        }
                        break;
                    case 'stop_loss':
                        if (input.value === '' || isNaN(input.value) || input.value <= 0) {
                            showError(input, 'Please enter a stop loss price.');
                            isValid = false;
                        }
                        break;
                    case 'cash_out':
                        if (input.value === '' || isNaN(input.value) || input.value <= 0) {
                            showError(input, 'Please enter a profit price');
                            isValid = false;
                        }
                        break;
                    case 'comment':
                        if (input.value === '') {
                            showError(input, 'Please enter trade note');
                            isValid = false;
                        }
                        break;
                    default:
                        break;
                }
            });
        console.log(isValid)
            // If all validations pass, submit the form
            if (isValid) {
            
            // Get the value of the toggle switch
            const yahooFinanceToggleValue = yahooFinanceToggle.checked ? 'on' : 'off';

            // Create a hidden input to store the toggle value
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'yahooFinance';
            hiddenInput.value = yahooFinanceToggleValue;

            // Append the hidden input to the form
            addStockForm.appendChild(hiddenInput);
            console.log("The Add Stock Form: ${addStockForm}")

            // Submit the form
            addStockForm.submit();
            }
        });
    }
});


// const jsonFilePath  = "static/json/tickers.json"
// Populate Dropdown for Demo Purpose
        document.addEventListener('DOMContentLoaded', function () {
            // Path to your JSON file
            const jsonFilePath  = "static/json/tickers";
        //    \static\json\tickers
            // Fetch the JSON file
            fetch(jsonFilePath)
                .then(response => response.json())
                .then(data => populateDropdown(data))
                .catch(error => console.error('Error loading JSON:', error));
            
            function populateDropdown(stocks) {
                console.log(stocks)
                const dropdown = document.getElementById('stockDropdown');
        
                // Iterate over the stocks and create an option element for each
                stocks.forEach(stock => {
                    console.log(stock)
                    const option = document.createElement('option');
                    option.value = stock.ticker; // Ticker as value
                    option.text = `(${stock.ticker}) : ${stock.name}`; // Display name of ticker
        
                    dropdown.appendChild(option); // Add option to dropdown
                });
            }
        });
        
 
// Function to display error messages
function showError(inputElement, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.color = 'red';
    errorElement.innerText = message;
    inputElement.parentElement.appendChild(errorElement);
}

// Function to clear previous error messages
function clearErrorMessages() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(function(message) {
        message.remove();
    });
}