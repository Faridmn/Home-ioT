$(document).ready(() => {
  $('#add_event_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'  : $('#add_event_device_list').val(),
      'event' : $('#add_event_type').val(),
      'at'    : encodeURI($('#add_event_at').val())
    };

    call_and_write_text('#add_event_form', formData);
  });
});
