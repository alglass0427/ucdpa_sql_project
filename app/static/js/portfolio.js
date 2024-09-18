$(document).ready(function() {
 
    $('#refreshButton').click(function() {
        var url = $(this).data('url');  // Get the URL from the data attribute
        let portfolio = document.getElementById('portfolioList').value;

        $.ajax({
            url: url,  // Use the URL from the data attribute
            type: 'POST',
            contentType: 'application/json',  // Specify content type as JSON
            data: JSON.stringify({ 'portfolio': portfolio }),
            success: function(response) {
                $('#portfolioDisplay').html(response);
            }
        });
    });
});
