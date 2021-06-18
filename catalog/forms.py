from django import forms


class OrderForm(forms.Form):
    buyer_name = forms.CharField(label="收货人姓名", max_length=20)
    buyer_address = forms.CharField(label="收货人地址", max_length=100)
    buyer_phone = forms.CharField(label="收货人手机号", max_length=13)
    remark = forms.CharField(label="备注", max_length=200, widget=forms.Textarea)
