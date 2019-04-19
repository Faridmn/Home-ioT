$(document).ready(() => {
  $('#remove_device_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'        : $('#remove_device_list').val()
    };

    call_and_write_text('#remove_device_form', formData);
  });
});
