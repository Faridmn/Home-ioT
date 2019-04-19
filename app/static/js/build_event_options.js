function build_event_options() {
  $.getJSON(
    '/get-device-events',
    {
      'uuid'   : $('#remove_event_device_list').val(),
      'from_ts': encodeURI($('1970-01-01T00:00:00Z').val())
    },
    data => {
      $('.event_list').find('option').remove();

      $.each(data, (key, val) => {
        const option_item = '<option value="' + val['uuid'] + ',' + val['at'] + '">'
                            + val['location'] + ' ' + val['name'] +  ' set to ' + val['event']
                            + ' at ' + val['at'] + '</option>';
        $('.event_list').append(option_item);
      });
    }
  );
}

$(document).ready(build_event_options());
