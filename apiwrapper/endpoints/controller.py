from apiwrapper.endpoints.annual_overview import AnnualOverview
from apiwrapper.endpoints.attachment_public import AttachmentPublic
from apiwrapper.endpoints.attachment_tab import AttachmentTab
from apiwrapper.endpoints.avatar import Avatar
from apiwrapper.endpoints.card import Card
from apiwrapper.endpoints.cash_register import CashRegister
from apiwrapper.endpoints.certificate_pinned import CertificatePinned
from apiwrapper.endpoints.chat_conversation import ChatConversation
from apiwrapper.endpoints.customer_statement import CustomerStatement
from apiwrapper.endpoints.device_server import DeviceServer
from apiwrapper.endpoints.draft_payment import DraftPayment
from apiwrapper.endpoints.draft_share_invite_bank import DraftShareInviteBank
from apiwrapper.endpoints.installation import Installation
from apiwrapper.endpoints.invoice import Invoice
from apiwrapper.endpoints.master_card_action import MasterCardAction
from apiwrapper.endpoints.monetary_account import MonetaryAccount
from apiwrapper.endpoints.payment import Payment
from apiwrapper.endpoints.request_inquiry import RequestInquiry
from apiwrapper.endpoints.schedule import Schedule
from apiwrapper.endpoints.scheduled_payment import ScheduledPayment
from apiwrapper.endpoints.session_server import SessionServer
from apiwrapper.endpoints.share_invite_bank_inquiry import \
    ShareInviteBankInquiry
from apiwrapper.endpoints.share_invite_bank_response import \
    ShareInviteBankResponse
from apiwrapper.endpoints.tab_attachment import TabAttachment
from apiwrapper.endpoints.user import User


class Controller:

    def __init__(self, api_client):
        self.installation = Installation(api_client)
        self.device_server = DeviceServer(api_client)
        self.session_server = SessionServer(api_client)
        self.user = User(api_client)
        self.monetary_account = MonetaryAccount(api_client)
        self.card = Card(api_client)
        self.payment = Payment(api_client)
        self.request_inquiry = RequestInquiry(api_client)
        self.draft_payment = DraftPayment(api_client)
        self.schedule = Schedule(api_client)
        self.scheduled_payment = ScheduledPayment(api_client)
        self.cash_register = CashRegister(api_client)
        self.master_card_action = MasterCardAction(api_client)
        self.chat_conversation = ChatConversation(api_client)
        self.certificate_pinned = CertificatePinned(api_client)
        self.invoice = Invoice(api_client)
        self.annual_overview = AnnualOverview(api_client)
        self.attachment_public = AttachmentPublic(api_client)
        self.attachment_tab = AttachmentTab(api_client)
        self.avatar = Avatar(api_client)
        self.customer_statement = CustomerStatement(api_client)
        self.draft_invite = DraftShareInviteBank(api_client)
        self.share_inquiry = ShareInviteBankInquiry(api_client)
        self.share_response = ShareInviteBankResponse(api_client)
        self.tab = TabAttachment(api_client)
