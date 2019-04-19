function actually_build(data, parent_node) {
  $.each(data, (key, val) => {
    const option_item = '<option value="' + val['uuid'] + '">' + val['location']
                      + ", " + val['name'] + '</option>';
    $(parent_node).append(option_item);
  });
}

function build_device_options() {
  $.getJSON(
    '/get-device',
    data => {
      $('.device_list').find('option').remove();

      actually_build(data, '.device_list');
    }
  );
}

function build_optional_device_options() {
  $.getJSON(
    '/get-device',
    data => {
      $('.optional_device_list').find('option').remove();

      const all_option = '<option value="">All Devices</option>';
      $('.optional_device_list').append(all_option);

      actually_build(data, '.optional_device_list');
    }
  );
}

$(document).ready(build_device_options());
$(document).ready(build_optional_device_options());
