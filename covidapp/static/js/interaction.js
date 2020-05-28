$(function () {
var checkout = $('#txtCheckOut').datepicker({autoclose: true, format: 'dd/M/yy'});
$('#txtCheckOut').attr('disabled', 'disabled');
var checkin = $('#txtCheckIn').datepicker({
    autoclose: true,
    format: 'dd/M/yy',
    startDate: "dd"
  }).on('changeDate', function(event) {
    $('#txtCheckOut').removeAttr('disabled');
    checkout.datepicker("setStartDate", event.date);

    $('#txtCheckOut')[0].focus();
  });
});
