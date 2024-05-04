$(document).ready(function(){
    // Clear modal input fields on close
    $('#addTimelineModal').on('hidden.bs.modal', function (e) {
        $(this).find('form')[0].reset();
    });
});

// Function to handle opening the edit modal
$(document).ready(function() {
    $('.edit-timeline-btn').click(function() {
        var timelineId = $(this).data('timeline-id');
        openEditModal(timelineId);
    });
    

    $('.edit-timeline-link').click(function(event) {
        event.preventDefault();
        var timelineId = $(this).data('timeline-id');
        openEditModal(timelineId);
    });
});

/// Function to handle opening the edit modal
function openEditModal(timelineId) {
    if (!timelineId) {
        console.error("Timeline ID is not defined.");
        console.log("Timeline ID:", timelineId);
        return;
    }

    // Set the timelineId value in the hidden input field
    $('#edit_timeline_id').val(timelineId);

    // Send AJAX request to fetch timeline data
    $.ajax({
        url: `/get-timeline/${timelineId}/`,
        type: "GET",
        success: function(response) {
            // Populate the edit modal fields with fetched timeline data
            $('#edit_event_title').val(response.event_title);
            $('#edit_event_description').val(response.event_description);
            $('#edit_date').val(response.date);
            $('#edit_time').val(response.time);

            // Show the modal
            $('#editTimelineModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
            // Handle error response
            // You may show an error message to the user here
        }
    });
}


// Function to handle form submission
function submitEditForm(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Retrieve the timeline_id from the hidden input field
    var timelineId = $('#edit_timeline_id').val();
    console.log("Timeline ID:", timelineId);

    // Check if timelineId is empty or undefined
    if (!timelineId) {
        console.error("Timeline ID is missing.");
        return; // Abort form submission
    }

    // Serialize form data
    var formData = $('#editTimelineForm').serialize();

    // Send AJAX request to handle form submission
    $.ajax({
        url: `/edit-timeline/${timelineId}/`,
        type: "POST",
        data: formData,
        success: function(response) {
            // Handle success response, e.g., close modal, update UI, etc.
            $('#editTimelineModal').modal('hide'); // Close modal
            // You may update the UI here if needed
        },
        error: function(xhr, status, error) {
            // Handle error response
            console.error(xhr.responseText);
            // You may show an error message to the user here
        }
    });
}
