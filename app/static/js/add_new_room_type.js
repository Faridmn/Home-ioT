$(document).ready(() => {
  $('#add_room_type_button').click((e) => {
    e.preventDefault();
    const formData = {
      'name' : $('#add_room_type_name').val(),
      'icon' : $('#add_room_type_icon').val(),
    };

    call_and_write_text('#add_room_type_form', formData);
  });
});
