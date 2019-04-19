$(document).ready(() => {
  $('#remove_event_button').click((e) => {
    e.preventDefault();
    const values = $('#remove_event_list').val().split(',')
    const formData = {
      'uuid' : values[0],
      'at'   : values[1]
    };

    call_and_write_text('#remove_event_form', formData);
  });
});
