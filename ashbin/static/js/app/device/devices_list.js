/**
 * Created by admin on 2016/3/30.
 */
$(document).ready(function() {
    $('.delete').click(function(event){
        if(confirm('Sure to Delete?')){
            var deviceId = $(this).data('device-id');
            var url = $(this).data('href');
            var tdDom = $(this).parent().parent();
            $.ajax({
                url: url,
                type: 'delete',
                success: function(res){
                    tdDom.remove();
                    console.log('delete success')
                },
                error: function(res){
                    console.log('delete failed')
                }
            })
        }
        console.log(deviceId)
    });
    var resource_url = window.location.href + '/resource';
    var oTable = $('#deviceTable').dataTable({
                "aLengthMenu": [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                "iDisplayLength": 15,
                "sDom": "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",
                "sPaginationType": "bootstrap",
                "oLanguage": {
                    "sLengthMenu": "_MENU_ records per page",
                    "oPaginate": {
                        "sPrevious": "Prev",
                        "sNext": "Next"
                    }
                },
                "aoColumnDefs": [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
            });

            jQuery('#deviceTable_wrapper .dataTables_filter input').addClass("form-control medium"); // modify table search input
            jQuery('#deviceTable_wrapper .dataTables_length select').addClass("form-control xsmall"); // modify table per page dropdown

} );