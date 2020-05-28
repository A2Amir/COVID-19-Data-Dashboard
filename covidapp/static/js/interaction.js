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

// plots the figure with id
// id must match the div id above in the html
var figures = {{figuresJSON | safe}};
var ids = {{ids | safe}};
for(var i in figures) {
      Plotly.plot(ids[i],
      figures[i].data,
      figures[i].layout || {});
}
