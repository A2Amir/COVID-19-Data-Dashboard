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

Plotly.setPlotConfig({
   mapboxAccessToken: "pk.eyJ1IjoiYW1pcnppYWVlIiwiYSI6ImNrYXNlZXd4eDBpcXAzMG1zOTR1NWt2bzUifQ.9vOmF1-LoxDggkQshH6sbQ"
 });
