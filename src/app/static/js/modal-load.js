$(document).on("click", ".open-modal-button", function () {
  var parts = $(this).data("url").split("_");
  var type = parts[0];
  var id = parts[1];

  $.ajax({
    type: "GET",
    url: "/edit/",
    data: { media_type: type, media_id: id },
    success: function (data) {
      var output = data.title;
      if (data.year) {
        output += " (" + data.year + ")";
      }

      if (data.original_type) {
        // capitalize first letter
        output += " ["
               + data.original_type.charAt(0).toUpperCase()
               + data.original_type.slice(1)
               + "]";
      } else if (data.media_type) {
        // capitalize first letter
        output += " ["
               + data.media_type.charAt(0).toUpperCase()
               + data.media_type.slice(1)
               + "]";
      }

      $("#modal-title-" + type + "_" + id).html(output);
      $("#modal-body-" + type + "_" + id).html(data.html);
      if (data.seasons) {
        var select = $("#season-select-" + type + "_" + id);

        new bootstrap.Tooltip(
          document
            .getElementById("season-descriptor-" + type + "_" + id)
            .querySelector('[data-bs-toggle="tooltip"]')
        );

        var score = $("#score-input-" + type + "_" + id);
        var status = $("#season-status-" + type + "_" + id);
        var progress = $("#progress-input-" + type + "_" + id);
        var start = $("#start-input-" + type + "_" + id);
        var end = $("#end-input-" + type + "_" + id);

        select.change(function () {
          var selectedValue = $(this).val();

          if (selectedValue == "general") {
            score.val(data.score);
            status.val(data.status);
            progress.val(data.progress);
            start.val(data.start_date);
            end.val(data.end_date);
          } else {
            let exists = false;

            // check if season exists in database
            for (let i = 0; i < data["media_seasons"].length && !exists; i++) {
              let media_season = data["media_seasons"][i];
              if (media_season.number == selectedValue) {
                score.val(media_season.score);
                status.val(media_season.status);
                progress.val(media_season.progress);
                start.val(media_season.start_date);
                end.val(media_season.end_date);
                exists = true;
              }
            }

            if (!exists) {
              score.val("");
              status.val("Completed");
              progress.val("");
              start.val("");
              end.val("");
            }
          }
        });
      }
      if (data.in_db) {
        // Add delete button if it doesn't exist
        if (
          $("#modal-footer-" + type + "_" + id + " .delete-btn").length == 0
        ) {
          var deleteButton = $(
            '<button class="btn btn-danger delete-btn" type="submit" name="delete">Delete</button>'
          );
          $("#modal-footer-" + type + "_" + id + " form").append(deleteButton);
        }
      }
    },
  });
});
