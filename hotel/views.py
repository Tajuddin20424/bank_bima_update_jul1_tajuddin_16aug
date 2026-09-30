from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection, transaction
from django.conf import settings
from django.utils import timezone

import os
import uuid
import traceback


# ============================================================
# HOTEL PAGE
# ============================================================

def hotel_view(request):

    return render(
        request,
        'hotel/guest_info.html'
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

def save_guest_image(image_file):

    if not image_file:
        return None

    allowed_extensions = [
        '.jpg',
        '.jpeg',
        '.png',
        '.webp'
    ]

    extension = os.path.splitext(
        image_file.name
    )[1].lower()

    if extension not in allowed_extensions:

        raise ValueError(
            'Only JPG, JPEG, PNG and WEBP images are allowed.'
        )

    if image_file.size > 5 * 1024 * 1024:

        raise ValueError(
            'Image size must be less than 5 MB.'
        )

    upload_dir = os.path.join(
        settings.MEDIA_ROOT,
        'hotel_guests'
    )

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    filename = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    relative_path = os.path.join(
        'hotel_guests',
        filename
    )

    full_path = os.path.join(
        settings.MEDIA_ROOT,
        relative_path
    )

    with open(
        full_path,
        'wb+'
    ) as destination:

        for chunk in image_file.chunks():

            destination.write(
                chunk
            )

    return relative_path.replace(
        os.sep,
        '/'
    )


# ============================================================
# DELETE IMAGE
# ============================================================

def delete_guest_image(image_path):

    if not image_path:
        return

    try:

        full_path = os.path.join(
            settings.MEDIA_ROOT,
            image_path
        )

        if os.path.isfile(full_path):

            os.remove(full_path)

    except Exception:

        pass


# ============================================================
# LOAD HOTEL GUEST
# ============================================================

def load_hotel(request):

    if request.method == 'GET':

        try:

            with connection.cursor() as cursor:

                sql = """
                    SELECT
                        id,
                        title,
                        guest_name,
                        image,
                        mobile,
                        gender,
                        date_of_birth,
                        nationality,
                        address,
                        check_in,
                        check_out,
                        booking_source,
                        guest_category,
                        Bed_Category,
                        bed_info,
                        emergency_guest_contact,
                        status
                    FROM hotel_guests_info
                    ORDER BY id ASC
                """

                cursor.execute(sql)

                rows = cursor.fetchall()


            hotel_list = []

            for row in rows:

                hotel_list.append({

                    'id': row[0],

                    'title': row[1] or '',

                    'guest_name': row[2] or '',

                    'image': row[3] or '',

                    'mobile': row[4] or '',

                    'gender': row[5] or '',

                    'date_of_birth': (
                        row[6].strftime('%Y-%m-%d')
                        if row[6]
                        else ''
                    ),

                    'nationality': row[7] or '',

                    'address': row[8] or '',

                    'check_in': (
                        row[9].strftime('%Y-%m-%dT%H:%M')
                        if row[9]
                        else ''
                    ),

                    'check_out': (
                        row[10].strftime('%Y-%m-%dT%H:%M')
                        if row[10]
                        else ''
                    ),

                    'booking_source': row[11] or '',

                    'guest_category': row[12] or '',

                    'bed_category': row[13] or '',

                    'bed_info': row[14] or '',

                    'emergency_guest_contact':
                        row[15] or '',

                    'status': row[16]

                })


            return JsonResponse({
                'status': 'success',
                'hotels': hotel_list
            })


        except Exception as e:

            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })



# ============================================================
# SAVE HOTEL GUEST
# ============================================================

def save_hotel(request):

    if request.method != "POST":

        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)


    try:

        data = request.POST

        current_now = timezone.now()


        # =====================================================
        # FORM DATA
        # =====================================================

        title = data.get(
            'title',
            ''
        ).strip()

        guest_name = data.get(
            'guest_name',
            ''
        ).strip()

        mobile = data.get(
            'mobile',
            ''
        ).strip()

        gender = data.get(
            'gender',
            ''
        ).strip()

        date_of_birth = data.get(
            'date_of_birth',
            ''
        ).strip()

        nationality = data.get(
            'nationality',
            ''
        ).strip()

        address = data.get(
            'address',
            ''
        ).strip()

        booking_source = data.get(
            'booking_source',
            ''
        ).strip()

        guest_category = data.get(
            'guest_category',
            ''
        ).strip()

        check_in = data.get(
            'check_in',
            ''
        ).strip()

        check_out = data.get(
            'check_out',
            ''
        ).strip()

        bed_category = data.get(
            'bed_category_id',
            ''
        ).strip()

        bed_info = data.get(
            'bed_info_id',
            ''
        ).strip()

        emergency_guest_contact = data.get(
            'emergency_guest_contact',
            ''
        ).strip()

        status = data.get(
            'status'
        ) or '1'

        image_file = request.FILES.get(
            'image'
        )


        # =====================================================
        # BASIC VALIDATION
        # =====================================================

        if not guest_name:

            return JsonResponse({
                'status': 'error',
                'message': 'Guest name is required'
            })


        if not mobile:

            return JsonResponse({
                'status': 'error',
                'message': 'Mobile is required'
            })


        # =====================================================
        # IMAGE
        # =====================================================

        image_path = None

        if image_file:

            image_path = save_guest_image(
                image_file
            )


        # =====================================================
        # DATABASE
        # =====================================================

        with transaction.atomic():

            with connection.cursor() as cursor:


                # =================================================
                # STEP A
                # GET GUEST TRANSACTION CONFIGURATION
                # =================================================

                cursor.execute("""
                    SELECT
                        id,
                        tran_method,
                        user_role

                    FROM transaction__withs

                    WHERE
                    (
                        LOWER(tran_with_name) LIKE '%%guest%%'
                    )

                    LIMIT 1
                """)


                tran_with_meta = cursor.fetchone()


                if tran_with_meta:

                    tran_with_id_val = tran_with_meta[0]

                    extracted_tran_method = (
                        tran_with_meta[1]
                        if tran_with_meta[1] is not None
                        else "Both"
                    )

                    extracted_user_role = (
                        tran_with_meta[2]
                        if tran_with_meta[2] is not None
                        else 4
                    )

                else:

                    tran_with_id_val = 0

                    extracted_tran_method = "Both"

                    extracted_user_role = 4


                    # =================================================
                # STEP B
                # UNIQUE GUEST USER ID
                #
                # GUEST000000001
                # GUEST000000002
                # =================================================

                cursor.execute("""
                    SELECT MAX(
                        CAST(
                            REPLACE(
                                REPLACE(user_id, 'GUEST-', ''),
                                'GUEST',
                                ''
                            ) AS UNSIGNED
                        )
                    )
                    FROM user__infos
                    WHERE user_id LIKE 'GUEST%%'
                """)


                last_user = cursor.fetchone()


                if last_user and last_user[0]:

                    new_number = int(last_user[0]) + 1

                else:

                    new_number = 1


                generated_user_id = (
                    f"GUEST{new_number:09d}"
                )


                print(
                    "GENERATED GUEST USER ID >>>>>>",
                    generated_user_id
                )


                                

                # =================================================
                # STEP C
                # SAVE INTO USER__INFOS
                # =================================================

                user_sql = """
                    INSERT INTO user__infos
                    (
                        user_id,
                        title,
                        user_name,
                        user_email,
                        user_phone,
                        gender,
                        dob,
                        nationality,
                        address,
                        user_role,
                        tran_user_type,
                        tran_method,
                        tran_with_id,
                        image,
                        status,
                        added_at
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """


                cursor.execute(
                    user_sql,
                    [
                        generated_user_id,

                        title or None,

                        guest_name,

                        None,

                        mobile,

                        gender or None,

                        date_of_birth or None,

                        nationality or None,

                        address or None,

                        extracted_user_role,

                        tran_with_id_val,

                        extracted_tran_method,

                        tran_with_id_val,

                        image_path,

                        status,

                        current_now
                    ]
                )


                # =================================================
                # USER INFO DATABASE ID
                # =================================================

                user_info_db_id = cursor.lastrowid


                # =================================================
                # STEP D
                # SAVE INTO HOTEL_GUESTS_INFO
                # =================================================

                hotel_sql = """
                    INSERT INTO hotel_guests_info
                    (
                        title,
                        guest_name,
                        image,
                        mobile,
                        gender,
                        date_of_birth,
                        nationality,
                        address,
                        booking_source,
                        guest_category,
                        check_in,
                        check_out,
                        Bed_Category,
                        bed_info,
                        emergency_guest_contact,
                        status
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """


                cursor.execute(
                    hotel_sql,
                    [
                        title or None,

                        guest_name,

                        image_path,

                        mobile,

                        gender or None,

                        date_of_birth or None,

                        nationality or None,

                        address or None,

                        booking_source or None,

                        guest_category or None,

                        check_in or None,

                        check_out or None,

                        bed_category or None,

                        bed_info or None,

                        emergency_guest_contact or None,

                        status
                    ]
                )


                # =================================================
                # NEW HOTEL GUEST ID
                # =================================================

                hotel_guest_id = cursor.lastrowid


                # =================================================
                # STEP E
                # AUTO SAVE CHECK IN DETAILS
                # =================================================

                check_in_sql = """
                    INSERT INTO check_in_details
                    (
                        hotel_guest_id,
                        bed_category_id,
                        bed_info_id,
                        check_in,
                        check_out,
                        remarks,
                        status
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """


                cursor.execute(
                    check_in_sql,
                    [
                        hotel_guest_id,

                        bed_category or None,

                        bed_info or None,

                        check_in or None,

                        check_out or None,

                        '',

                        status
                    ]
                )


                # =================================================
                # STEP F
                # AUTO BED OCCUPIED
                # =================================================

                cursor.execute("""
                    UPDATE bed_info

                    SET occupancy = 'occupied'

                    WHERE id = %s
                """, [
                    bed_info
                ])


        # =====================================================
        # SUCCESS
        # =====================================================

        return JsonResponse({

            'status': 'success',

            'message':
                'Guest information saved successfully',

            'guest_id':
                hotel_guest_id,

            'user_info_id':
                user_info_db_id,

            'user_id':
                generated_user_id

        })


    except Exception as e:

        print(
            "========== HOTEL GUEST SAVE ERROR =========="
        )

        traceback.print_exc()

        print(
            "============================================"
        )


        return JsonResponse({

            'status': 'error',

            'message': str(e)

        }, status=400)

# ============================================================
# UPDATE HOTEL GUEST
# ============================================================

def update_hotel(request):

    if request.method == 'POST':

        try:

            guest_db_id = request.POST.get(
                'id',
                ''
            ).strip()


            title = request.POST.get(
                'title',
                ''
            ).strip()

            guest_name = request.POST.get(
                'guest_name',
                ''
            ).strip()

            mobile = request.POST.get(
                'mobile',
                ''
            ).strip()

            gender = request.POST.get(
                'gender',
                ''
            ).strip()

            date_of_birth = request.POST.get(
                'date_of_birth',
                ''
            ).strip()

            nationality = request.POST.get(
                'nationality',
                ''
            ).strip()

            address = request.POST.get(
                'address',
                ''
            ).strip()

            booking_source = request.POST.get(
                'booking_source',
                ''
            ).strip()

            guest_category = request.POST.get(
                'guest_category',
                ''
            ).strip()


            # =================================================
            # CHECK IN / CHECK OUT WITH TIME
            # =================================================

            check_in = request.POST.get(
                'check_in',
                ''
            ).strip()

            check_out = request.POST.get(
                'check_out',
                ''
            ).strip()


            bed_category = request.POST.get(
                'bed_category_id',
                ''
            ).strip()

            bed_info = request.POST.get(
                'bed_info_id',
                ''
            ).strip()

            emergency_guest_contact = request.POST.get(
                'emergency_guest_contact',
                ''
            ).strip()

            status = request.POST.get(
                'status'
            ) or '1'

            image_file = request.FILES.get(
                'image'
            )


            if not guest_db_id:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Database ID is missing'
                })


            if not guest_name:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Guest name is required'
                })


            if not mobile:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Mobile is required'
                })


            # =================================================
            # GET OLD IMAGE
            # =================================================

            with connection.cursor() as cursor:

                sql = """
                    SELECT
                        image
                    FROM hotel_guests_info
                    WHERE id = %s
                """

                cursor.execute(
                    sql,
                    [guest_db_id]
                )

                row = cursor.fetchone()


            if not row:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Guest not found'
                })


            old_image = row[0]


            # =================================================
            # UPDATE WITH IMAGE
            # =================================================

            if image_file:

                new_image_path = save_guest_image(
                    image_file
                )


                with connection.cursor() as cursor:

                    sql = """
                        UPDATE hotel_guests_info
                        SET
                            title = %s,
                            guest_name = %s,
                            image = %s,
                            mobile = %s,
                            gender = %s,
                            date_of_birth = %s,
                            nationality = %s,
                            address = %s,
                            booking_source = %s,
                            guest_category = %s,
                            check_in = %s,
                            check_out = %s,
                            Bed_Category = %s,
                            bed_info = %s,
                            emergency_guest_contact = %s,
                            status = %s
                        WHERE id = %s
                    """

                    params = [
                        title or None,
                        guest_name,
                        new_image_path,
                        mobile,
                        gender or None,
                        date_of_birth or None,
                        nationality or None,
                        address or None,
                        booking_source or None,
                        guest_category or None,

                        check_in or None,
                        check_out or None,

                        bed_category or None,
                        bed_info or None,
                        emergency_guest_contact or None,
                        status,
                        guest_db_id
                    ]

                    cursor.execute(
                        sql,
                        params
                    )


                if old_image:

                    delete_guest_image(
                        old_image
                    )


            # =================================================
            # UPDATE WITHOUT IMAGE
            # =================================================

            else:

                with connection.cursor() as cursor:

                    sql = """
                        UPDATE hotel_guests_info
                        SET
                            title = %s,
                            guest_name = %s,
                            mobile = %s,
                            gender = %s,
                            date_of_birth = %s,
                            nationality = %s,
                            address = %s,
                            booking_source = %s,
                            guest_category = %s,
                            check_in = %s,
                            check_out = %s,
                            Bed_Category = %s,
                            bed_info = %s,
                            emergency_guest_contact = %s,
                            status = %s
                        WHERE id = %s
                    """

                    params = [
                        title or None,
                        guest_name,
                        mobile,
                        gender or None,
                        date_of_birth or None,
                        nationality or None,
                        address or None,
                        booking_source or None,
                        guest_category or None,

                        check_in or None,
                        check_out or None,

                        bed_category or None,
                        bed_info or None,
                        emergency_guest_contact or None,
                        status,
                        guest_db_id
                    ]

                    cursor.execute(
                        sql,
                        params
                    )


            # =================================================
            # CHECK CHECK IN DETAILS
            # =================================================

            with connection.cursor() as cursor:

                sql = """
                    SELECT id
                    FROM check_in_details
                    WHERE hotel_guest_id = %s
                """

                cursor.execute(
                    sql,
                    [guest_db_id]
                )

                check_in_row = cursor.fetchone()


                # =============================================
                # UPDATE CHECK IN DETAILS
                # =============================================

                if check_in_row:

                    sql = """
                        UPDATE check_in_details
                        SET
                            bed_category_id = %s,
                            bed_info_id = %s,
                            check_in = %s,
                            check_out = %s,
                            status = %s
                        WHERE hotel_guest_id = %s
                    """

                    params = [
                        bed_category,
                        bed_info,

                        check_in or None,
                        check_out or None,

                        status,
                        guest_db_id
                    ]

                    cursor.execute(
                        sql,
                        params
                    )


                # =============================================
                # INSERT IF NOT EXISTS
                # =============================================

                else:

                    sql = """
                        INSERT INTO check_in_details
                        (
                            hotel_guest_id,
                            bed_category_id,
                            bed_info_id,
                            check_in,
                            check_out,
                            remarks,
                            status
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                    """

                    params = [
                        guest_db_id,
                        bed_category,
                        bed_info,

                        check_in or None,
                        check_out or None,

                        '',
                        status
                    ]

                    cursor.execute(
                        sql,
                        params
                    )


            return JsonResponse({
                'status': 'success',
                'message':
                    'Guest information updated successfully'
            })


        except Exception as e:

            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })


# ============================================================
# DELETE HOTEL GUEST
# ============================================================

def delete_hotel(request):

    if request.method == 'POST':

        try:

            guest_db_id = request.POST.get(
                'id',
                ''
            ).strip()


            if not guest_db_id:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Database ID is missing'
                })


            # =================================================
            # GET IMAGE
            # =================================================

            with connection.cursor() as cursor:

                sql = """
                    SELECT image
                    FROM hotel_guests_info
                    WHERE id = %s
                """

                cursor.execute(
                    sql,
                    [guest_db_id]
                )

                row = cursor.fetchone()


            if not row:

                return JsonResponse({
                    'status': 'error',
                    'message': 'Guest not found'
                })


            image_path = row[0]


            # =================================================
            # DELETE CHECK IN
            # =================================================

            with connection.cursor() as cursor:

                sql = """
                    DELETE FROM check_in_details
                    WHERE hotel_guest_id = %s
                """

                cursor.execute(
                    sql,
                    [guest_db_id]
                )


                # =============================================
                # DELETE HOTEL GUEST
                # =============================================

                sql = """
                    DELETE FROM hotel_guests_info
                    WHERE id = %s
                """

                cursor.execute(
                    sql,
                    [guest_db_id]
                )


            if image_path:

                delete_guest_image(
                    image_path
                )


            return JsonResponse({
                'status': 'success',
                'message':
                    'Guest information deleted successfully'
            })


        except Exception as e:

            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request'
    })