$(document).ready(function () {
        $("#txtFromDate").datepicker({
            format: 'dd/mm/yyyy',
            autoclose: 1,
            //startDate: new Date(),
            todayHighlight: false,
            //endDate: new Date()
        }).on('changeDate', function (selected) {
            var minDate = new Date(selected.date.valueOf());
            $('#txtToDate').datepicker('setStartDate', minDate);
            $("#txtToDate").val($("#txtFromDate").val());
            $(this).datepicker('hide');
        });

        $("#txtToDate").datepicker({
            format: 'dd/mm/yyyy',
            todayHighlight: true,
            //endDate: new Date()
        }).on('changeDate', function (selected) {
            $(this).datepicker('hide');
        });
    });
