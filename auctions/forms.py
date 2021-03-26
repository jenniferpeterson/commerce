from django import forms

from .models import User, Category, Auction_Listing


class NewListingForm(forms.Form):

    title = forms.CharField(label="Listing Name", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.URLField(label="Image", widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    starting_bid = forms.DecimalField(label="Starting Bid", widget=forms.NumberInput(
        attrs={'class': 'form-control'}
    ))


class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Your Bid", widget=forms.NumberInput(
        attrs={'class': 'form-control'}))


class AddCommentForm(forms.Form):
    comment_title = forms.CharField(label="Comment Title", widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    comment = forms.CharField(label="Comment", widget=forms.Textarea(
        attrs={'class': 'form-control'}))
