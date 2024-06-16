$(document).ready(function () {
  $('#download-form').on('submit', function (e) {
    e.preventDefault();
    const videoUrl = $('#video-url').val();
    if (videoUrl) {
      $('#message').html(
        '<div class="alert alert-info">Processing your request...</div>'
      );

      $.ajax({
        url: 'http://localhost:5000/download', // Adjust this to match your backend endpoint
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ url: videoUrl }),
        success: function (response) {
          if (response.success) {
            $('#message').html(
              '<div class="alert alert-success">Video downloaded successfully!</div>'
            );
            // Provide a link to download the video
            $('#message').append(
              `<a href="${response.download_link}" class="btn btn-success mt-2">Download Video</a>`
            );
          } else {
            $('#message').html(
              '<div class="alert alert-danger">' + response.error + '</div>'
            );
          }
        },
        error: function () {
          $('#message').html(
            '<div class="alert alert-danger">An error occurred while processing your request.</div>'
          );
        },
      });
    } else {
      $('#message').html(
        '<div class="alert alert-danger">Please enter a valid YouTube URL.</div>'
      );
    }
  });
});
