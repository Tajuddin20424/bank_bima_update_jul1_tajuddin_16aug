
let mode = "save";


// ============================================================
// LOAD HOTEL GUEST INFO
// ============================================================

function loadHotel() {

    $.ajax({

        url: '/hotel/load-hotel/',
        method: 'GET',

        success: function(response) {

            console.log("Hotel Data:", response);

            let hotels = response.hotels || [];
            let tbody = '';


            if (hotels.length === 0) {

                tbody = `
                    <tr>
                        <td
                            colspan="7"
                            class="text-center text-muted"
                        >
                            No Guest Found
                        </td>
                    </tr>
                `;

                $('#guestTableBody').html(tbody);

                return;
            }


            $.each(hotels, function(index, h) {


                // =================================================
                // STATUS
                // =================================================

                let statusBadge = h.status == 1
                    ? '<span class="badge bg-success">Active</span>'
                    : '<span class="badge bg-danger">Inactive</span>';


                // =================================================
                // IMAGE
                // =================================================

                let image = '';

                if (h.image) {

                    image = `
                        <img
                            src="/media/${h.image}"
                            width="50"
                            height="50"
                            style="
                                object-fit: cover;
                                border-radius: 50%;
                            "
                        >
                    `;

                } else {

                    image = 'No Image';

                }


                // =================================================
                // TABLE ROW
                // =================================================

                tbody += `

                    <tr
                        class="hotel-row"

                        data-id="${h.id}"

                        data-title="${h.title || ''}"

                        data-guest_name="${h.guest_name || ''}"

                        data-mobile="${h.mobile || ''}"

                        data-gender="${h.gender || ''}"

                        data-date_of_birth="${h.date_of_birth || ''}"

                        data-nationality="${h.nationality || ''}"

                        data-address="${h.address || ''}"

                        data-check_in="${h.check_in || ''}"

                        data-check_out="${h.check_out || ''}"

                        data-booking_source="${h.booking_source || ''}"

                        data-guest_category="${h.guest_category || ''}"

                        data-bed_category="${h.bed_category || ''}"

                        data-bed_info="${h.bed_info || ''}"

                        data-emergency_guest_contact="${h.emergency_guest_contact || ''}"

                        data-status="${h.status || ''}"
                    >

                        <td>
                            ${index + 1}
                        </td>

                        <td>
                            ${image}
                        </td>

                        <td>
                            ${h.title || ''}
                            ${h.guest_name || ''}
                        </td>

                        <td>
                            ${h.mobile || ''}
                        </td>

                        <td>
                            ${h.bed_category || ''}
                        </td>

                        <td>
                            ${statusBadge}
                        </td>

                        <td>

                            <button
                                type="button"
                                class="btn btn-sm btn-warning editBtn"
                                data-id="${h.id}"
                            >
                                Edit
                            </button>

                            <button
                                type="button"
                                class="btn btn-sm btn-danger deleteBtn"
                                data-id="${h.id}"
                                data-name="${h.guest_name || ''}"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>
                `;

            });


            $('#guestTableBody').html(
                tbody
            );

        },


        error: function(xhr) {

            console.log(
                xhr.responseText
            );

            alert(
                "Failed to load hotel guest list."
            );

        }

    });

}


// ============================================================
// DOCUMENT READY
// ============================================================

$(document).ready(function() {


    // ========================================================
    // LOAD HOTEL
    // ========================================================

    loadHotel();


    // ========================================================
    // SAVE / UPDATE
    // ========================================================

    $('#saveBtn').on(
        'click',
        function(e) {

            e.preventDefault();


            // =================================================
            // GET FORM VALUES
            // =================================================

            let id =
                $('#guest_db_id').val();


            let title =
                $('#title').val();


            let guest_name =
                $('#guest_name').val();


            let mobile =
                $('#mobile').val();


            let gender =
                $('#gender').val();


            let date_of_birth =
                $('#date_of_birth').val();


            let nationality =
                $('#nationality').val();

            let address =
                $('#address').val();


            let check_in =
                $('#check_in').val();


            let check_out =
                $('#check_out').val();


            let booking_source =
                $('#booking_source').val();


            let guest_category =
                $('#guest_category').val();


            // =================================================
            // BED CATEGORY
            // =================================================

            let bed_category_id =
                $('#bed_category_id').val();


            // =================================================
            // BED INFO
            // =================================================

            let bed_info_id =
                $('#bed_info_id').val();


            // =================================================
            // EMERGENCY CONTACT
            // =================================================

            let emergency_contact =
                $('#emergency_contact').val();


            let status =
                $('#status').val();



            // =================================================
            // VALIDATION
            // =================================================

            if (!guest_name) {

                alert(
                    "Please enter guest name."
                );

                return;
            }


            if (!mobile) {

                alert(
                    "Please enter mobile number."
                );

                return;
            }


            if (!bed_category_id) {

                alert(
                    "Please select bed category."
                );

                return;
            }


            if (!bed_info_id) {

                alert(
                    "Please select bed."
                );

                return;
            }



            // =================================================
            // FORM DATA
            // =================================================

            let formData =
                new FormData();


            formData.append(
                'title',
                title
            );


            formData.append(
                'guest_name',
                guest_name
            );


            formData.append(
                'mobile',
                mobile
            );


            formData.append(
                'gender',
                gender
            );


            formData.append(
                'date_of_birth',
                date_of_birth
            );


            formData.append(
                'nationality',
                nationality
            );


            formData.append(
                'address',
                address
            );


            formData.append(
                'check_in',
                check_in
            );


            formData.append(
                'check_out',
                check_out
            );


            formData.append(
                'booking_source',
                booking_source
            );


            formData.append(
                'guest_category',
                guest_category
            );


            // =================================================
            // IMPORTANT
            // =================================================

            formData.append(
                'bed_category_id',
                bed_category_id
            );


            formData.append(
                'bed_info_id',
                bed_info_id
            );


            // =================================================
            // IMPORTANT
            // =================================================

            formData.append(
                'emergency_guest_contact',
                emergency_contact
            );


            formData.append(
                'status',
                status
            );



            // =================================================
            // IMAGE
            // =================================================

            let imageInput =
                $('#image')[0];


            if (
                imageInput &&
                imageInput.files &&
                imageInput.files.length > 0
            ) {

                formData.append(
                    'image',
                    imageInput.files[0]
                );

            }



            // =================================================
            // DEBUG
            // =================================================

            console.log(
                "Title:",
                title
            );

            console.log(
                "Bed Category ID:",
                bed_category_id
            );

            console.log(
                "Bed Info ID:",
                bed_info_id
            );



            // =================================================
            // SAVE
            // =================================================

            if (mode === 'save') {

                $.ajax({

                    url:
                        '/hotel/save-hotel/',

                    method:
                        'POST',

                    headers: {

                        "X-CSRFToken":
                            csrftoken

                    },

                    data:
                        formData,

                    processData:
                        false,

                    contentType:
                        false,


                    success: function(response) {

                        console.log(
                            "Save Response:",
                            response
                        );


                        if (
                            response.status ===
                            'success'
                        ) {

                            alert(
                                response.message ||
                                "Saved successfully"
                            );


                            loadHotel();


                            clearHotelForm();

                        }

                        else {

                            alert(
                                response.message ||
                                "Save failed"
                            );

                        }

                    },


                    error: function(xhr) {

                        console.log(
                            xhr.responseText
                        );


                        let message =
                            "Server error while saving guest.";


                        if (
                            xhr.responseJSON &&
                            xhr.responseJSON.message
                        ) {

                            message =
                                xhr.responseJSON.message;

                        }


                        alert(
                            message
                        );

                    }

                });

            }



            // =================================================
            // UPDATE
            // =================================================

            else if (
                mode === 'update'
            ) {


                if (!id) {

                    alert(
                        "Guest ID not found."
                    );

                    return;

                }


                formData.append(
                    'id',
                    id
                );


                $.ajax({

                    url:
                        '/hotel/update-hotel/',

                    method:
                        'POST',

                    headers: {

                        "X-CSRFToken":
                            csrftoken

                    },

                    data:
                        formData,

                    processData:
                        false,

                    contentType:
                        false,


                    success: function(response) {

                        console.log(
                            "Update Response:",
                            response
                        );


                        if (
                            response.status ===
                            'success'
                        ) {

                            alert(
                                response.message ||
                                "Updated successfully"
                            );


                            loadHotel();


                            clearHotelForm();

                        }

                        else {

                            alert(
                                response.message ||
                                "Update failed"
                            );

                        }

                    },


                    error: function(xhr) {

                        console.log(
                            xhr.responseText
                        );


                        let message =
                            "Server error while updating guest.";


                        if (
                            xhr.responseJSON &&
                            xhr.responseJSON.message
                        ) {

                            message =
                                xhr.responseJSON.message;

                        }


                        alert(
                            message
                        );

                    }

                });

            }

        }
    );

});



// ============================================================
// EDIT HOTEL GUEST
// ============================================================

$(document).on(
    'click',
    '.editBtn',
    function(e) {

        e.preventDefault();


        let id =
            $(this).data('id');


        console.log(
            "Editing Guest ID:",
            id
        );


        $.ajax({

            url:
                '/hotel/load-hotel/',

            method:
                'GET',


            success: function(response) {

                let hotels =
                    response.hotels || [];


                // =============================================
                // FIND SELECTED GUEST
                // =============================================

                let guest =
                    hotels.find(
                        function(h) {

                            return String(h.id) ===
                                   String(id);

                        }
                    );


                if (!guest) {

                    alert(
                        "Guest information not found."
                    );

                    return;

                }


                console.log(
                    "Edit Guest:",
                    guest
                );


                // =============================================
                // UPDATE MODE
                // =============================================

                mode =
                    "update";


                // =============================================
                // ID
                // =============================================

                $('#guest_db_id').val(
                    guest.id
                );


                // =============================================
                // TITLE
                // =============================================

                $('#title').val(
                    guest.title || ''
                );


                // =============================================
                // GUEST NAME
                // =============================================

                $('#guest_name').val(
                    guest.guest_name || ''
                );


                // =============================================
                // MOBILE
                // =============================================

                $('#mobile').val(
                    guest.mobile || ''
                );


                // =============================================
                // GENDER
                // =============================================

                $('#gender').val(
                    guest.gender || ''
                );


                // =============================================
                // DATE OF BIRTH
                // =============================================

                $('#date_of_birth').val(
                    guest.date_of_birth || ''
                );


                // =============================================
                // NATIONALITY
                // =============================================

                $('#nationality').val(
                    guest.nationality || ''
                );

                // =============================================
                // ADDRESS
                // =============================================

                $('#address').val(
                    guest.address || ''
                );


                // =============================================
                // CHECK IN
                // =============================================

                $('#check_in').val(
                    guest.check_in || ''
                );


                // =============================================
                // CHECK OUT
                // =============================================

                $('#check_out').val(
                    guest.check_out || ''
                );


                // =============================================
                // BOOKING SOURCE
                // =============================================

                $('#booking_source').val(
                    guest.booking_source || ''
                );


                // =============================================
                // GUEST CATEGORY
                // =============================================

                $('#guest_category').val(
                    guest.guest_category || ''
                );


                // =============================================
                // BED CATEGORY
                // =============================================

                $('#bed_category_id').val(
                    guest.bed_category || ''
                );


                // =============================================
                // EMERGENCY CONTACT
                // =============================================

                $('#emergency_contact').val(
                    guest.emergency_guest_contact || ''
                );


                // =============================================
                // STATUS
                // =============================================

                $('#status').val(
                    String(
                        guest.status == null
                            ? '1'
                            : guest.status
                    )
                );


                // =============================================
                // BED INFO
                // =============================================

                if (
                    typeof loadBedInfoCombo ===
                    'function'
                ) {

                    loadBedInfoCombo(
                        guest.bed_info || ''
                    );

                }

                else {

                    $('#bed_category_id').trigger(
                        'change'
                    );


                    setTimeout(
                        function() {

                            $('#bed_info_id').val(
                                guest.bed_info || ''
                            );

                        },
                        500
                    );

                }


                // =============================================
                // IMAGE PREVIEW
                // =============================================

                if (guest.image) {

                    $('#imagePreview')
                        .attr(
                            'src',
                            '/media/' +
                            guest.image
                        )
                        .show();

                }

                else {

                    $('#imagePreview')
                        .attr(
                            'src',
                            ''
                        )
                        .hide();

                }


                $('#image').val('');


                // =============================================
                // BUTTON
                // =============================================

                $('#saveBtn').text(
                    'Update'
                );

            },


            error: function(xhr) {

                console.log(
                    xhr.responseText
                );


                alert(
                    "Failed to load guest information."
                );

            }

        });

    }
);



// ============================================================
// DELETE HOTEL GUEST
// ============================================================

$(document).on(
    'click',
    '.deleteBtn',
    function(e) {

        e.preventDefault();


        const guest_id =
            $(this).data('id');


        const guest_name =
            $(this).data('name');


        if (
            confirm(
                "Confirm to remove " +
                guest_name +
                "?"
            )
        ) {

            $.ajax({

                url:
                    '/hotel/delete-hotel/',

                method:
                    'POST',

                headers: {

                    "X-CSRFToken":
                        csrftoken

                },

                data: {

                    'id':
                        guest_id

                },

                dataType:
                    'json',


                success: function(response) {

                    console.log(
                        "Delete Response:",
                        response
                    );


                    if (
                        response.status ===
                        'success'
                    ) {

                        alert(
                            response.message ||
                            "Guest removed successfully!"
                        );


                        loadHotel();


                        if (
                            String(
                                $('#guest_db_id').val()
                            ) ===
                            String(
                                guest_id
                            )
                        ) {

                            clearHotelForm();

                        }

                    }

                    else {

                        alert(
                            response.message ||
                            "Delete failed"
                        );

                    }

                },


                error: function(
                    xhr,
                    status,
                    error
                ) {

                    console.log(
                        xhr.responseText
                    );


                    alert(
                        "Server error: " +
                        error
                    );

                }

            });

        }

    }
);



// ============================================================
// TITLE → GENDER
// ============================================================

$(document).on(
    'change',
    '#title',
    function() {

        let title =
            $(this).val();


        if (
            title === 'Mr.' ||
            title === 'Shri'
        ) {

            $('#gender').val(
                'Male'
            );

        }

        else if (
            title === 'Mrs.' ||
            title === 'Ms.' ||
            title === 'Miss' ||
            title === 'Shrimati'
        ) {

            $('#gender').val(
                'Female'
            );

        }

        else {

            $('#gender').val('');

        }

    }
);

// ============================================================
// CLEAR GUEST INFO FORM
// ============================================================

$(document).on('click', '#clearBtn', function(e) {

    e.preventDefault();

    $('#guest_db_id').val('');

    $('#title').val('');
    $('#guest_name').val('');
    $('#mobile').val('');
    $('#gender').val('');
    $('#date_of_birth').val('');
    $('#nationality').val('');
    $('#address').val('');
    $('#booking_source').val('');
    $('#guest_category').val('');

    $('#bed_category_id').val('');
    $('#bed_info_id').html(
        '<option value="">Select Bed Info</option>'
    );

    $('#check_in').val('');
    $('#check_out').val('');

    $('#emergency_contact').val('');
    $('#status').val('1');

    $('#image').val('');
    $('#imagePreview').attr('src', '').hide();

    mode = 'save';

    $('#saveBtn').text('Save');

});