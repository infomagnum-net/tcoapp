# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0023_auto_20161109_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='S3Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SKU', models.CharField(help_text=b'Please enter SKU', max_length=200, null=True, blank=True)),
                ('OfferTermCode', models.CharField(help_text=b'Please enter SKU', max_length=200, null=True, blank=True)),
                ('RateCode', models.CharField(help_text=b'Please enter SKU', max_length=200, null=True, blank=True)),
                ('termstype', models.CharField(help_text=b'Please enter SKU', max_length=200, null=True, blank=True)),
                ('PriceDescription', models.TextField(null=True, blank=True)),
                ('EffectiveDate', models.CharField(help_text=b'EffectiveDate', max_length=200, null=True, blank=True)),
                ('StartingRange', models.IntegerField(help_text=b'Please enter StartingRange ', null=True, blank=True)),
                ('EndingRange', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('Unit', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('price_per_unit', models.DecimalField(help_text=b'The price per unit.', max_digits=19, decimal_places=4, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('currency', models.CharField(default=b'USD', help_text=b'The currency in which the subscription will be charged.', max_length=4, choices=[('AED', 'UAE Dirham'), ('AFN', 'Afghani'), ('ALL', 'Lek'), ('AMD', 'Armenian Dram'), ('ANG', 'Netherlands Antillian Guilder'), ('AOA', 'Kwanza'), ('ARS', 'Argentine Peso'), ('AUD', 'Australian Dollar'), ('AWG', 'Aruban Guilder'), ('AZN', 'Azerbaijanian Manat'), ('BAM', 'Convertible Marks'), ('BBD', 'Barbados Dollar'), ('BDT', 'Taka'), ('BGN', 'Bulgarian Lev'), ('BHD', 'Bahraini Dinar'), ('BIF', 'Burundi Franc'), ('BMD', 'Bermudian Dollar'), ('BND', 'Brunei Dollar'), ('BOB', 'Boliviano'), ('BOV', 'Mvdol'), ('BRL', 'Brazilian Real'), ('BSD', 'Bahamian Dollar'), ('BTN', 'Ngultrum'), ('BWP', 'Pula'), ('BYR', 'Belarussian Ruble'), ('BZD', 'Belize Dollar'), ('CAD', 'Canadian Dollar'), ('CDF', 'Congolese Franc'), ('CHE', 'WIR Euro'), ('CHF', 'Swiss Franc'), ('CHW', 'WIR Franc'), ('CLF', 'Unidades de fomento'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('COU', 'Unidad de Valor Real'), ('CRC', 'Costa Rican Colon'), ('CUP', 'Cuban Peso'), ('CVE', 'Cape Verde Escudo'), ('CYP', 'Cyprus Pound'), ('CZK', 'Czech Koruna'), ('DJF', 'Djibouti Franc'), ('DKK', 'Danish Krone'), ('DOP', 'Dominican Peso'), ('DZD', 'Algerian Dinar'), ('EEK', 'Kroon'), ('EGP', 'Egyptian Pound'), ('ERN', 'Nakfa'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FJD', 'Fiji Dollar'), ('FKP', 'Falkland Islands Pound'), ('GBP', 'Pound Sterling'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Dalasi'), ('GNF', 'Guinea Franc'), ('GTQ', 'Quetzal'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Lempira'), ('HRK', 'Croatian Kuna'), ('HTG', 'Gourde'), ('HUF', 'Forint'), ('IDR', 'Rupiah'), ('ILS', 'New Israeli Sheqel'), ('INR', 'Indian Rupee'), ('IQD', 'Iraqi Dinar'), ('IRR', 'Iranian Rial'), ('ISK', 'Iceland Krona'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('JPY', 'Yen'), ('KES', 'Kenyan Shilling'), ('KGS', 'Som'), ('KHR', 'Riel'), ('KMF', 'Comoro Franc'), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Tenge'), ('LAK', 'Kip'), ('LBP', 'Lebanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('LRD', 'Liberian Dollar'), ('LSL', 'Loti'), ('LTL', 'Lithuanian Litas'), ('LVL', 'Latvian Lats'), ('LYD', 'Libyan Dinar'), ('MAD', 'Moroccan Dirham'), ('MDL', 'Moldovan Leu'), ('MGA', 'Malagasy Ariary'), ('MKD', 'Denar'), ('MMK', 'Kyat'), ('MNT', 'Tugrik'), ('MOP', 'Pataca'), ('MRO', 'Ouguiya'), ('MTL', 'Maltese Lira'), ('MUR', 'Mauritius Rupee'), ('MVR', 'Rufiyaa'), ('MWK', 'Kwacha'), ('MXN', 'Mexican Peso'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MYR', 'Malaysian Ringgit'), ('MZN', 'Metical'), ('NAD', 'Namibia Dollar'), ('NGN', 'Naira'), ('NIO', 'Cordoba Oro'), ('NOK', 'Norwegian Krone'), ('NPR', 'Nepalese Rupee'), ('NZD', 'New Zealand Dollar'), ('OMR', 'Rial Omani'), ('PAB', 'Balboa'), ('PEN', 'Nuevo Sol'), ('PGK', 'Kina'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistan Rupee'), ('PLN', 'Zloty'), ('PYG', 'Guarani'), ('QAR', 'Qatari Rial'), ('RON', 'New Leu'), ('RSD', 'Serbian Dinar'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SAR', 'Saudi Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychelles Rupee'), ('SDG', 'Sudanese Pound'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Leone'), ('SOS', 'Somali Shilling'), ('SRD', 'Surinam Dollar'), ('STD', 'Dobra'), ('SVC', 'El Salvador Colon'), ('SYP', 'Syrian Pound'), ('SZL', 'Lilangeni'), ('THB', 'Baht'), ('TJS', 'Somoni'), ('TMM', 'Manat'), ('TND', 'Tunisian Dinar'), ('TOP', "Pa'anga"), ('TRY', 'New Turkish Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TWD', 'New Taiwan Dollar'), ('TZS', 'Tanzanian Shilling'), ('UAH', 'Hryvnia'), ('UGX', 'Uganda Shilling'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('USS', 'US Dollar (Same day)'), ('UYI', 'Uruguay Peso en Unidades Indexadas'), ('UYU', 'Peso Uruguayo'), ('UZS', 'Uzbekistan Sum'), ('VEF', 'Bolivar Fuerte'), ('VND', 'Dong'), ('VUV', 'Vatu'), ('WST', 'Tala'), ('XAF', 'CFA Franc BEAC'), ('XAG', 'Silver'), ('XAU', 'Gold'), ('XBA', 'European Composite Unit (EURCO)'), ('XBB', 'European Monetary Unit (E.M.U.-6)'), ('XBC', 'European Unit of Account 9 (E.U.A.-9)'), ('XBD', 'European Unit of Account 17 (E.U.A.-17)'), ('XCD', 'East Caribbean Dollar'), ('XDR', 'Special Drawing Rights'), ('XFO', 'Gold-Franc'), ('XFU', 'UIC-Franc'), ('XOF', 'CFA Franc BCEAO'), ('XPD', 'Palladium'), ('XPF', 'CFP Franc'), ('XPT', 'Platinum'), ('XTS', 'Code for testing purposes'), ('XXX', 'No currency'), ('YER', 'Yemeni Rial'), ('ZAR', 'Rand'), ('ZMK', 'Zambian Kwacha'), ('ZWD', 'Zimbabwe Dollar')])),
                ('Product_Family', models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True)),
                ('serviceCode', models.CharField(help_text=b'Please enter serviceCode', max_length=200, null=True, blank=True)),
                ('region', models.CharField(help_text=b'Please enter region', max_length=200, null=True, blank=True)),
                ('Location_Type', models.CharField(help_text=b'Please enter Location Type', max_length=200, null=True, blank=True)),
                ('Availability', models.DecimalField(null=True, max_digits=19, decimal_places=4, blank=True)),
                ('Storage_class', models.CharField(help_text=b'Please enter Storage Class', max_length=200, null=True, blank=True)),
                ('Volume_Type', models.CharField(help_text=b'Please enter Volume Type', max_length=200, null=True, blank=True)),
                ('Fee_Code', models.CharField(help_text=b'Please enter Volume Type', max_length=200, null=True, blank=True)),
                ('Fee_Description', models.CharField(help_text=b'Please enter Volume Type', max_length=200, null=True, blank=True)),
                ('Group', models.CharField(help_text=b'Please enter Group', max_length=200, null=True, blank=True)),
                ('Group_Description', models.CharField(help_text=b'Please enter Group_Description', max_length=200, null=True, blank=True)),
                ('Transfer_Type', models.CharField(help_text=b'Please enter Transfer_Type', max_length=200, null=True, blank=True)),
                ('From_Location', models.CharField(help_text=b'Please enter From_Location', max_length=200, null=True, blank=True)),
                ('From_Location_Type', models.CharField(help_text=b'Please enter From_Location_Type', max_length=200, null=True, blank=True)),
                ('To_Location', models.CharField(help_text=b'Please enter To_Location', max_length=200, null=True, blank=True)),
                ('To_Location_Type', models.CharField(help_text=b'Please enter To_Location_Type', max_length=200, null=True, blank=True)),
                ('usageType', models.CharField(help_text=b'Please enter usageType', max_length=200, null=True, blank=True)),
                ('operation', models.CharField(help_text=b'Please enter operation', max_length=200, null=True, blank=True)),
                ('Durability', models.DecimalField(null=True, max_digits=19, decimal_places=4, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='rds',
            name='EndingRange',
            field=models.CharField(help_text=b'Please enter Product Family', max_length=200, null=True, blank=True),
        ),
    ]
