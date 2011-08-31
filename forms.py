from django import forms


class AddressField(forms.CharField):
    def clean(self, value):
        forms.CharField(self, value)

        if value:
            signature = []
            for part in value.split("."):
                try:
                    part = int(part)
                    assert part > -1 and part < 256
                except (ValueError, AssertionError):
                    signature.append(False)
                else:
                    signature.append(True)

            if signature != [True] * 4:
                raise forms.ValidationError(
                    "Please enter a number in nnn.nnn.nnn.nnn format.")

        return value


class SubnetForm(forms.Form):
    address = AddressField(required=False)
    hostname = forms.CharField(required=False)
    mask = AddressField(required=False, label="Subnet (Mask)")
    cidr = forms.IntegerField(required=False, label="Subnet (CIDR)")
    num_hosts = forms.IntegerField(required=False)
    num_hosts.widget.attrs["readonly"] = "readonly"
    network = AddressField(required=False, label="Subnet ID")
    first_host = forms.CharField(required=False)
    first_host.widget.attrs["readonly"] = "readonly"
    last_host = forms.CharField(required=False)
    last_host.widget.attrs["readonly"] = "readonly"
    broadcast = forms.CharField(required=False)
    broadcast.widget.attrs["readonly"] = "readonly"
