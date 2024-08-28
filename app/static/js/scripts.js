document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded.');
});


setTimeout(function() {
    var flashMessages = document.getElementsByClassName('flash-message');
    for (var i = 0; i < flashMessages.length; i++) {
        flashMessages[i].style.display = 'none';
    }
}, 3000); // 3000 milliseconds = 5 seconds

let isModal = document.querySelectorAll(".modal_link")

isModal.forEach(stockItem => {
    // Add a click event listener to each item
    stockItem.addEventListener('click', () => {
     // Get the ID of the clicked element (e.g., AAPL, MSFT)
    console.log(stockItem.innerHTML)
     let stockCode = stockItem.textContent;
    console.log(stockCode);
    stock_modal = stockCode.concat("_modal");
    console.log(stock_modal);
    // Display the modal
    let modal = document.getElementById(stock_modal);
    console.log(modal)
    setTimeout(() => {
        modal.open()
    }, 200);
    

})})

// isModal.forEach(stockItem => {
//     // Add a click event listener to each item
//     stockItem.addEventListener('click', () => {
//         // Get the stock code from the clicked element's text content
//         let stockCode = stockItem.textContent.trim();
//         console.log(stockCode);  // Log the stock code (e.g., TSLA)

//         // Construct the modal's ID
//         let stock_modal = stockCode + "_modal";
//         console.log(stock_modal);  // Log the constructed modal ID

//         // Select the modal by ID
//         let modal = document.getElementById(stock_modal);
//         console.log(modal);  // Log the modal element to verify it's correctly selected

//         // Check if the modal exists before trying to open it
//         if (modal) {
//             setTimeout(() => {
//                 modal.open();  // Call the open method on the modal
//             }, 200);
//         } else {
//             console.error(`Modal with ID ${stock_modal} not found.`);
//         }
//     });
// });