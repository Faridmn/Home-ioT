$(document).ready(() => {
  $('#inspect_device_button').click((e) => {
    e.preventDefault();
    const formData = {
      'uuid'    : $('#inspect_device_list').val(),
    };

    call_and_write_list('#inspect_device_form', formData);
  });
});
