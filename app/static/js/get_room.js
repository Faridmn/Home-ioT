$(document).ready(() => {
  $('#inspect_room_button').click((e) => {
    e.preventDefault();
    const formData = {
      'name'    : $('#inspect_room_list').val(),
    };

    call_and_write_list('#inspect_room_form', formData)
  });
});
