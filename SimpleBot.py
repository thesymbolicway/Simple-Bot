from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from authorizenet.apicontrollers import getMerchantDetailsController

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')

def process_payment(amount, card_number, expiration_date, card_code):
    """
    A function to process payment through Authorize.Net
    """
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = '6Z888MnLbwF7'
    merchantAuth.transactionKey = '5u3AH3KyZ9zZ56SZ'

    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = card_number
    creditCard.expirationDate = expiration_date
    creditCard.cardCode = card_code

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = amount
    transactionrequest.payment = payment

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "MerchantID-0001"
    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if response is not None:
        return response.transactionResponse
    else:
        return None
    
def pay(update: Update, context: CallbackContext) -> None:
    # Example card details for testing in sandbox mode.
    test_card_number = "4111111111111111"
    test_expiration_date = "2030-12"
    test_card_code = "123"

    # Example payment amount
    payment_amount = 1.00

    # Process payment
    try:
        transaction_response = process_payment(payment_amount, test_card_number, test_expiration_date, test_card_code)
        
        # Debugging line to check the API response
        print(transaction_response)

        # Your existing condition check, but ensure the attribute exists.
        if transaction_response is not None and hasattr(transaction_response, 'responseCode') and transaction_response.responseCode == "1":
            update.message.reply_text('Payment successful!')
        else:
            update.message.reply_text('Payment failed! Please try again.')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        update.message.reply_text('An error occurred while processing the payment. Please try again later.')
        

def get_merchant_details():
    """
    Function to ping Authorize.Net API with getMerchantDetailsRequest 
    to verify that the API Login ID and Transaction Key are valid.
    """

    # Create a merchantAuthenticationType object with authentication details
    merchantAuth = apicontractsv1.merchantAuthenticationType()  
    merchantAuth.name = '6Z888MnLbwF7'
    merchantAuth.transactionKey = '5u3AH3KyZ9zZ56SZ'

    # Create request and set merchantAuthentication
    request = apicontractsv1.getMerchantDetailsRequest()
    request.merchantAuthentication = merchant_auth
    
    # Create controller and execute the request
    controller = getMerchantDetailsController(request)
    controller.execute()

    # Get the response
    response = controller.getresponse()

    # Check response and display result
    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print("Successfully got merchant details")
            print("Merchant Name: %s" % response.merchantName)
            print("Gateway Id: %s" % response.gatewayId)
        else:
            print("ERROR: %s" % response.messages.message[0]['text'].text)
    else:
        print("Null Response Received")
        
def main() -> None:
    # Replace YOUR_NEW_TOKEN with your actual token.
    updater = Updater("6548003260:AAFAPr8lTjOPxdVHV1r8T9rTjfFaVI3QHBw", use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pay", pay))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
