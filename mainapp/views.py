import io
import json
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from xhtml2pdf import pisa

from mainapp.decorators import editdetails_authentication
from mainapp.forms import EditUserDetailsForm, UserChangePasswordCustom, AddBlogForm, EditBlogForm, AddUserForm, \
    AddAppointment, EditAppointment, AddCustomePaymentMethodForm, AddOrderForm, AddProductForm, AddProductImageForm, \
    EditProductForm
from mainapp.models import User, Blogs, Appointments, PtoSNotification, StoPNotification, StoDNotification, \
    DtoPNotification, Products, CartProductInfo, Cart, CustomePaymentMethod, OrderProductInfo, Orders, ProductImage

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime


def allnotification(request):
    ptosns = None
    stopns = None
    stodns = None
    dtopns = None
    ncount = None

    if request.user.is_staff or request.user.is_hospital_staff:
        ptosns = PtoSNotification.objects.all()
        if ptosns:
            ncount = ptosns.count()

    if request.user.is_patient:
        stopns = StoPNotification.objects.filter(patient=request.user.username)
        dtopns = DtoPNotification.objects.filter(patient=request.user.username)
        if stopns and dtopns:
            ncount = int(stopns.count()) + int(dtopns.count())
        elif stopns and not dtopns:
            ncount = stopns.count()
        elif dtopns and not stopns:
            ncount = dtopns.count()
    if request.user.is_doctor:
        stodns = StoDNotification.objects.filter(doctor=request.user.username)
        if stodns:
            ncount = stodns.count()

    return {'ptosns': ptosns,
            'stopns': stopns,
            'stodns': stodns,
            'dtopns': dtopns,
            'ncount': ncount}


@login_required(login_url='login')
def home(request):
    blogs = Blogs.objects.filter(blog_publish=True).order_by('-blog_pubdate')[:3]
    objnotify = allnotification(request)

    context = {
        'blogs': blogs,
        'objnotify': objnotify
    }
    return render(request, 'index.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            loginUsername = request.POST.get('loginUsername')
            loginPassword = request.POST.get('loginPassword')

            user = authenticate(request, username=loginUsername, password=loginPassword)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_profile(request, pid1):
    objnotify = allnotification(request)
    user = User.objects.get(id=pid1)
    context = {'user': user, 'objnotify': objnotify}
    return render(request, 'user_profile.html', context)


@editdetails_authentication
def user_edit_details(request, pid1):
    objnotify = allnotification(request)
    user = User.objects.get(id=pid1)
    form = EditUserDetailsForm(instance=user)

    if request.method == 'POST':
        form = EditUserDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            user_new_info = form.save(commit=False)

            user.first_name = user_new_info.first_name
            user.last_name = user_new_info.last_name
            user.email = user_new_info.email
            user.user_mobile = user_new_info.user_mobile
            user.user_address = user_new_info.user_address
            if not user_new_info.user_image == '':
                user.user_image = user_new_info.user_image

            user.save()
            return redirect('user_profile', pid1)
    context = {'form': form, 'user': user, 'objnotify': objnotify}
    return render(request, 'user_edit_details.html', context)


@editdetails_authentication
def user_change_password(request, pid1):
    pid1 = pid1
    user = User.objects.get(id=pid1)
    objnotify = allnotification(request)

    form = UserChangePasswordCustom(user)
    if request.method == 'POST':
        form = UserChangePasswordCustom(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pid1)
    context = {'form': form, 'user': user, 'objnotify': objnotify}
    return render(request, 'user_change_password.html', context)


def article(request):
    objnotify = allnotification(request)
    blogs = Blogs.objects.filter(blog_publish=True).order_by('-blog_pubdate')
    context = {'blogs': blogs, 'objnotify': objnotify}
    return render(request, 'articles.html', context)


def single_article(request, slug):
    objnotify = allnotification(request)

    blog = Blogs.objects.get(blog_slug=slug)
    context = {'blog': blog, 'objnotify': objnotify}
    return render(request, 'single_article.html', context)


def add_article(request):
    objnotify = allnotification(request)

    form = AddBlogForm()

    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.blog_pubdate = datetime.now()
            newform.save()
            return redirect('articles')
    context = {'form': form, 'objnotify': objnotify}
    return render(request, 'add_article.html', context)


def edit_article(request, earid):
    objnotify = allnotification(request)

    blog = Blogs.objects.get(id=earid)
    form = EditBlogForm(instance=blog)

    if request.method == 'POST':
        form = EditBlogForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            blog.blog_title = newform.blog_title
            blog.blog_slug = newform.blog_slug
            blog.blog_desc = newform.blog_desc
            if not newform.blog_img == 'emptyfile':
                blog.blog_img = newform.blog_img
            blog.blog_publish = newform.blog_publish
            blog.save()
            return redirect('articles')
    context = {'form': form, 'blogobj': blog, 'objnotify': objnotify}
    return render(request, 'edit_article.html', context)


def hospital_staff(request):
    objnotify = allnotification(request)

    users_staff = User.objects.filter(is_hospital_staff=True)

    context = {'users_staff': users_staff, 'objnotify': objnotify}
    return render(request, 'hospital_staff.html', context)


def add_hospital_staff(request):
    objnotify = allnotification(request)

    form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.is_hospital_staff = True
            newform.save()
            return redirect('hospital-staff')
    context = {'form': form, 'objnotify': objnotify}
    return render(request, 'add_hospital_staff.html', context)


def hospital_doctors(request):
    objnotify = allnotification(request)

    users_doctor = User.objects.filter(is_doctor=True)

    context = {'users_doctor': users_doctor, 'objnotify': objnotify}
    return render(request, 'hospital_doctors.html', context)


def add_hospital_doctor(request):
    objnotify = allnotification(request)

    form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.is_doctor = True
            newform.save()
            return redirect('hospital-doctors')
    context = {'form': form, 'objnotify': objnotify}
    return render(request, 'add_hospital_doctor.html', context)


def hospital_patients(request):
    objnotify = allnotification(request)

    users_patient = User.objects.filter(is_patient=True)
    context = {'users_patient': users_patient, 'objnotify': objnotify}
    return render(request, 'hospital_patients.html', context)


def add_hospital_patient(request):
    objnotify = allnotification(request)

    form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.is_patient = True
            newform.save()
            return redirect('hospital-patients')
    context = {'form': form, 'objnotify': objnotify}
    return render(request, 'add_hospital_patient.html', context)


def appointments(request):
    objnotify = allnotification(request)

    objapnmts = None
    if request.user.is_staff or request.user.is_hospital_staff:
        objapnmts = Appointments.objects.all()
    elif request.user.is_patient:
        objapnmts = Appointments.objects.filter(patient__username=request.user.username)
    elif request.user.is_doctor:
        objapnmts = Appointments.objects.filter(doctor__username=request.user.username)

    context = {'objapnmts': objapnmts, 'objnotify': objnotify}
    return render(request, 'appointments.html', context)


def add_appointment(request):
    objnotify = allnotification(request)

    form = AddAppointment()
    if request.method == 'POST':
        form = AddAppointment(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.patient = request.user
            newform.save()
            ptosnobj = PtoSNotification.objects.create(appointment_id=newform.id, patient=newform.patient.username)
            ptosnobj.save()
            return redirect('appointments')
    context = {'form': form, 'objnotify': objnotify}
    return render(request, 'add_appointment.html', context)


def edit_appointment(request, eaid):
    objnotify = allnotification(request)

    objapnmt = Appointments.objects.get(id=eaid)
    form = EditAppointment(instance=objapnmt)
    if request.method == 'POST':
        form = EditAppointment(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            if request.user.username == objapnmt.patient.username:
                print('patient')
                objapnmt.p_h_problem = newform.p_h_problem
            elif request.user.is_hospital_staff:
                print('hospital staff')
                if objapnmt.a_status == '1':
                    if newform.a_status == '2' or newform.a_status == '3':
                        objapnmt.a_status = newform.a_status
                        stopnobj = StoPNotification.objects.create(appointment_id=objapnmt.id,
                                                                   patient=objapnmt.patient.username,
                                                                   status=newform.get_a_status_display())
                        stopnobj.save()
                    if newform.a_status == '3':
                        print('ok')
                        stodnobj = StoDNotification.objects.create(appointment_id=objapnmt.id,
                                                                   doctor=objapnmt.doctor.username)
                        stodnobj.save()

                objapnmt.a_date_time = newform.a_date_time
                objapnmt.checkup_report_file = newform.checkup_report_file

            elif request.user.username == objapnmt.doctor.username:
                print('doctor')
                if not objapnmt.a_status == '4':
                    if newform.a_status == '4':
                        objapnmt.a_status = newform.a_status
                objapnmt.a_date_time = newform.a_date_time
                objapnmt.checkup_report_file = newform.checkup_report_file
                objapnmt.a_meeting_id = newform.a_meeting_id
                objapnmt.checkup_report = newform.checkup_report
                objapnmt.d_prescription = newform.d_prescription
            elif request.user.is_staff:
                print('admin')
                if objapnmt.a_status == '1':
                    if newform.a_status == '2' or newform.a_status == '3':
                        objapnmt.a_status = newform.a_status

                        stopnobj = StoPNotification.objects.create(appointment_id=objapnmt.id,
                                                                   patient=objapnmt.patient.username,
                                                                   status=newform.get_a_status_display())
                        stopnobj.save()
                    if newform.a_status == '3':
                        stodnobj = StoDNotification.objects.create(appointment_id=objapnmt.id,
                                                                   doctor=objapnmt.doctor.username)
                        stodnobj.save()
                objapnmt.p_h_problem = newform.p_h_problem
                objapnmt.a_date_time = newform.a_date_time
                objapnmt.checkup_report_file = newform.checkup_report_file
                objapnmt.a_meeting_id = newform.a_meeting_id
                objapnmt.checkup_report = newform.checkup_report
                objapnmt.d_prescription = newform.d_prescription

            objapnmt.save()
            return redirect('appointments')
    context = {'form': form, 'objapnmt': objapnmt, 'objnotify': objnotify}
    return render(request, 'edit_appointment.html', context)


def deleteptosnotify(request, ptosid):
    objptosn = PtoSNotification.objects.get(id=ptosid)
    objptosn.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deletestopnotify(request, stopid):
    objstopn = StoPNotification.objects.get(id=stopid)
    objstopn.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deletestodnotify(request, stodid):
    objstodn = StoDNotification.objects.get(id=stodid)
    objstodn.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def meeting(request, aidm):
    objnotify = allnotification(request)

    objapnmt = Appointments.objects.get(id=aidm)
    context = {'objapnmt': objapnmt, 'objnotify': objnotify}
    return render(request, 'meetingpage.html', context)


def invite_patient(request):
    if request.method == 'POST':
        apnmt_id = request.POST.get('apid')
        apnmt_m_id = request.POST.get('apmid')
        objapnmt = Appointments.objects.get(id=int(apnmt_id))

        dtopobj = DtoPNotification.objects.create(appointment_id=objapnmt.id, doctor=objapnmt.doctor.username,
                                                  patient=objapnmt.patient.username, meeting_id=apnmt_m_id)
        dtopobj.save()
        return HttpResponse('Invitation Sent')
    else:
        return HttpResponse('wrong')


def deletedtopnotify(request, dtopid):
    objdtopn = DtoPNotification.objects.get(id=dtopid)
    objdtopn.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def registerpatient(request):
    form = AddUserForm()

    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.is_patient = True
            newform.save()
            return redirect('login')
    context = {'form': form, }
    return render(request, 'register.html', context)


def pharmacy(request):
    objnotify = allnotification(request)
    product = Products.objects.all()

    """page = request.GET.get('page', 1)

    paginator = Paginator(product, 6)  # 6 show product per page
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)"""
    context = {"products": product, 'objnotify': objnotify}
    return render(request, 'pharmacy.html', context)


def cart(request):
    objnotify = allnotification(request)
    if request.method == 'POST':
        products_cart = request.POST.get('product_cart')
        products_cart = json.loads(products_cart)
        if products_cart:
            cart_obj = Cart.objects.create()
            final_total = Decimal('0.0')
            for c_product in products_cart:
                product_id = c_product
                product = Products.objects.get(id=product_id)
                product_qtty = products_cart[c_product][0]
                single_price = product.product_price
                total_price = single_price * int(product_qtty)
                cpi_obj = CartProductInfo.objects.create(product=product, product_quantity=product_qtty,
                                                         single_product_price=single_price,
                                                         total_product_price=total_price)
                cpi_obj.save()
                cart_obj.products_cart.add(cpi_obj)
                final_total = final_total + Decimal(total_price)
            print("okay")
            cart_obj.cart_total = Decimal(final_total)
            cart_obj.save()
            return redirect('checkout', cart_obj.id)
        else:
            return redirect('cart')

    context = {'objnotify': objnotify}
    return render(request, 'cart.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def checkout(request, cartid):
    objnotify = allnotification(request)
    cart_obj = Cart.objects.get(id=cartid)
    form = AddOrderForm()
    payment_form = AddCustomePaymentMethodForm()

    if request.method == 'POST':
        form = AddOrderForm(request.POST, request.FILES)
        payment_form = AddCustomePaymentMethodForm(request.POST, request.FILES)
        if form.is_valid() and payment_form.is_valid():
            newform = form.save(commit=False)
            newpaymentform = payment_form.save(commit=False)

            order_obj = Orders.objects.create(customer_name=newform.customer_name,
                                              customer_address=newform.customer_address,
                                              customer_contry=newform.customer_contry,
                                              customer_state=newform.customer_state,
                                              customer_city=newform.customer_city,
                                              city_zip=newform.city_zip,
                                              customer_email=newform.customer_email,
                                              customer_mobile_number=newform.customer_mobile_number)

            final_total = Decimal('0.0')
            for c_product in cart_obj.products_cart.all():
                product_id = c_product.product.id
                product = Products.objects.get(id=product_id)
                oder_prod_info_obj = OrderProductInfo.objects.create(product=product,
                                                                     product_quantity=c_product.product_quantity,
                                                                     single_product_price=c_product.single_product_price,
                                                                     total_product_price=c_product.total_product_price)
                oder_prod_info_obj.save()
                order_obj.products.add(oder_prod_info_obj)
                final_total = final_total + c_product.total_product_price

            order_obj.order_status = "1"
            order_obj.order_payment_type = "3"
            order_obj.order_payment_status = "2"
            order_obj.total_order_price = final_total

            order_payment = CustomePaymentMethod.objects.create(upi_transaction_id=newpaymentform.upi_transaction_id,
                                                                upi_id=newpaymentform.upi_id,
                                                                payment_proof=newpaymentform.payment_proof)
            order_payment.save()
            order_obj.custom_payment_ref = order_payment
            order_obj.save()
            """context = {'order_obj': order_obj}
            pdf = render_to_pdf('pdfbill.html', context)
            # rendering the template
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = str(order_obj.id) + '.pdf'
            content = 'attachment; filename="%s"' % filename
            response['Content-Disposition'] = content
            return response"""
            context = {"ordersuccess": True, "orderid": order_obj.id, 'objnotify': objnotify}
            return render(request, 'checkout.html', context)
            # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

    context = {"cart_obj": cart_obj, "form": form, "payment_form": payment_form, 'objnotify': objnotify}
    return render(request, 'checkout.html', context)

def orderbillpdf(request,oid):
    order_obj = Orders.objects.get(id=oid)
    context = {'order_obj': order_obj}
    pdf = render_to_pdf('pdfbill.html', context)
    # rendering the template
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = str(order_obj.id) + '.pdf'
    content = 'attachment; filename="%s"' % filename
    response['Content-Disposition'] = content
    return response

def ordertracking(request):
    objnotify = allnotification(request)
    if request.method == 'POST':
        orderid = request.POST.get('orderid')
        emailid = request.POST.get('emailid')
        context = {}
        if orderid and emailid:
            order_obj = Orders.objects.filter(id=orderid, customer_email=emailid)
            if order_obj:
                for order_obj in order_obj:
                    order_obj = order_obj
                context = {"orderstatus": True, 'order_obj': order_obj}
            else:
                context = {"orderstatus": False}
        else:
            context = {"orderstatus": False}

        return render(request, 'ordertrackingdetails.html', context)

    context = {'objnotify': objnotify}
    return render(request, 'ordertracking.html', context)


def pharmacy_single_product(request, slug):
    objnotify = allnotification(request)
    product = Products.objects.get(product_slug=slug)

    context = {"product": product, 'objnotify': objnotify}
    return render(request, 'pharmacy_single_product.html', context)


def pharmacy_add_product(request):
    objnotify = allnotification(request)

    form = AddProductForm()

    addproductformset = formset_factory(AddProductImageForm)
    productimgtf = {
        'productimg-TOTAL_FORMS': '0',
        'productimg-INITIAL_FORMS': '0',
        'productimg-MIN_NUM_FORMS': '0',
    }
    productformset = addproductformset(productimgtf, prefix='productimg')

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        productformset = addproductformset(request.POST, request.FILES, prefix='productimg')
        if form.is_valid():
            newform = form.save(commit=False)
            newform.save()

            print(productformset.is_valid)
            if productformset.is_valid():
                print('ok')
                for product_add_form in productformset:
                    prod_img = product_add_form.cleaned_data.get("product_images")
                    prod_img_obj = ProductImage.objects.create(product=newform, product_images=prod_img)
                    prod_img_obj.save()

            return redirect('pharmacy')
    context = {'form': form, 'objnotify': objnotify, 'productformset': productformset, }
    return render(request, 'add_product_pharmacy.html', context)


def pharmacy_edit_product(request, epid):
    objnotify = allnotification(request)
    product = Products.objects.get(id=epid)

    form = EditProductForm(instance=product)

    """editproductformset = formset_factory(AddProductImageForm)
    productimgtf = {
        'productimg-TOTAL_FORMS': '0',
        'productimg-INITIAL_FORMS': '0',
        'productimg-MIN_NUM_FORMS': '0',
    }

    print('ddd',product.productimage_set.all().count())
    productimgtf = {'productimg-TOTAL_FORMS': str(product.productimage_set.all().count()),
                     'productimg-INITIAL_FORMS': '0',
                     'productimg-MIN_NUM_FORMS': '0', }
    num = 0
    pi = ProductImage.objects.filter(product=product)
    for l in pi:
        print('aa',l)
        productimgtf['productimg-' + str(num) + '-product_images'] = l
        num = num + 1
    productformset = editproductformset(productimgtf,prefix='productimg')"""
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            product.product_title = newform.product_title
            product.product_title = newform.product_title
            product.product_price = newform.product_price
            product.product_desc = newform.product_desc
            product.product_count = newform.product_count

            if not newform.product_img == 'emptyfile':
                product.product_img = newform.product_img

            product.save()

            """productformset = editproductformset(request.POST, request.FILES, prefix='productimg')
            print(productformset.is_valid)
            if productformset.is_valid():
                print('ok')
                ProductImage.objects.filter(product__id=product.id).delete()
                for product_add_form in productformset:
                    prod_img = product_add_form.cleaned_data.get("product_images")
                    prod_img_obj = ProductImage.objects.create(product=newform, product_images=prod_img)
                    prod_img_obj.save()"""

            return redirect('pharmacy')
    context = {'form': form, 'objnotify': objnotify, }
    return render(request, 'edit_product_pharmacy.html', context)


def bill(request):
    order_obj = Orders.objects.get(id=17)
    context = {"orderstatus": True, 'order_obj': order_obj}
    return render(request, 'pdfbill.html', context)
