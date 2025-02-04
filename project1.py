
"""
Author: Rishi Jeswani
Date: September 24, 2024
Class: CSC295(002)

Program calculates and outputs the details of a mortgage, including monthly payments, and amortization table. 
It allows for user input of home purchase price, loan term, and down payment.

Functions defined: 
make_table_header():
    Calls a function from the `table_header` module to generate and print the table header.

output_loan_info(loan_type):
    Prints the loan type and associated APR from the `rate_dict` module.

get_PMI(purchase_price, down_payment):
    Calculates the monthly mortgage payment and PMI based on the provided home purchase price and down payment.
main():
    Main function for executing the mortgage calculation.
    Prompts the user for input values like purchase price, loan term, and down payment. 
    Calculates the loan amount, LTV ratio, monthly mortgage payment, and PMI, 
    and outputs a detailed payment schedule with interest, principal, and PMI breakdown.
    
"""
import rate_dict
import table_header
# Declare loan_type, loan_term as a global variable as they are used in between functions.
loan_type = ""
loan_term  = 0
YEAR_MONTH = 12
YEAR_LIST = [10,15,20,30]

def make_table_header():
    """
    Calls a function from the `table_header` module to generate and print the table header.
    """
    table_header.make_table_header()

def output_loan_info(loan_type):
    """
    Prints the loan type and associated APR from the `rate_dict` module.
    """
    print("Loan type:", end=" ")
    print(loan_type, end=" ")
    print(f"at {rate_dict.rates[loan_type]}% APR")


def get_PMI(purchase_price, down_payment): 
    """
    This function is passed the purchase price and down payment percentage as float
    values and returns the monthly payment.
    """
    global loan_type, loan_term

    # Calculate loan amount
    loan_amount = purchase_price - down_payment
    annual_interest_rate = rate_dict.rates[loan_type]

    # Convert annual interest rate to a monthly rate
    monthly_interest_rate = (annual_interest_rate / 100) / YEAR_MONTH
    # Total number of monthly payments
    num_payments = loan_term * YEAR_MONTH

    # Monthly payment formula (standard mortgage formula)
    monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)

    return monthly_payment

def main():
    """
    Main function for executing the mortgage calculation.
    Prompts the user for input values like purchase price, loan term, and down payment. 
    Calculates the loan amount, LTV ratio, monthly mortgage payment, and PMI, 
    and outputs a detailed payment schedule with interest, principal, and PMI breakdown.
    Also check for Validation for negative and invalid inputs.
    Mortgage summary at the end with totals for interest, principal, and PMI paid.
    Raises A Value error when non-numeric values are entered for purchase price, loan term, or down payment.
    """
    global loan_term, loan_type
    try:
        # Taking user input
        purchase_price = float(input("Enter the purchase price of your home: $"))
        while (purchase_price < 0):
            purchase_price = float(input("Enter a valid number for the purchase price of your home: $"))   
        loan_term = int(input("Enter the term of the loan in years: "))
        while loan_term not in YEAR_LIST:
            loan_term = int(input("Enter a valid term: "))
        down_payment_percentage = float(input("Enter your down payment percentage: "))
        while (down_payment_percentage < 0 or down_payment_percentage > 100):
            down_payment_percentage = float(input("Enter a valid down payment percentage: "))

        down_payment = (down_payment_percentage / 100) * purchase_price
        loan_amount = purchase_price - down_payment
        #neatness
        print("\n")
        print(f"Loan amount: ${loan_amount:,.2f}")

        # Calculate LTV ratio
        LTV_ratio = (loan_amount / purchase_price) * 100
        # To generate the key to access elemenrts rate dictionary 
        if LTV_ratio >= 90.1 and LTV_ratio <= 100 and loan_term == 10:
            loan_type = f"{loan_term}-Year Fixed, 90.1-100% LTV"
        elif LTV_ratio >= 80.1 and LTV_ratio < 90.1 and loan_term == 10:
            loan_type = f"{loan_term}-Year Fixed, 80.1-90% LTV"
        elif LTV_ratio < 80.1 and loan_term == 10:
            loan_type = f"{loan_term}-Year Fixed, 80% or less LTV"
        elif LTV_ratio >= 90.1 and LTV_ratio <= 100 and loan_term == 15:
            loan_type = f"{loan_term}-Year Fixed, 90.1-100% LTV"
        elif LTV_ratio < 90.1 and loan_term == 15:
            loan_type = f"{loan_term}-Year Fixed, 90% or less LTV"
        elif LTV_ratio >= 90.1 and LTV_ratio <= 100 and loan_term == 20:
            loan_type = f"{loan_term}-Year Fixed, 90.1-100% LTV"
        elif LTV_ratio < 90.1 and loan_term == 20:
            loan_type = f"{loan_term}-Year Fixed, 90% or less LTV"
        elif LTV_ratio >= 90.1 and LTV_ratio <= 100 and loan_term == 30:
            loan_type = f"{loan_term}-Year Fixed, 90.1-100% LTV"
        elif LTV_ratio < 90.1 and loan_term == 30:
            loan_type = f"{loan_term}-Year Fixed, 90% or less LTV"
        #print the loan type
        output_loan_info(loan_type)

        # Calculate monthly payment 
        monthly_payment = get_PMI(purchase_price, down_payment)
        print(f"Monthly Payment = ${monthly_payment:.2f}")

        # calculating PMI rate based on LTV ratio
        if LTV_ratio > 95 and LTV_ratio <= 100:
            pmi_rate = 1.030 / 100  
        elif LTV_ratio > 90 and LTV_ratio <= 95:
            pmi_rate = 0.875 / 100  
        elif LTV_ratio > 85 and LTV_ratio <= 90:
            pmi_rate = 0.675 / 100  
        elif LTV_ratio > 80 and LTV_ratio <= 85:
            pmi_rate = 0.375 / 100  
        else:
            pmi_rate = 0.0  # No PMI for LTV <= 80%
       
        # Calculate PMI (monthly)
        pmi_payment = (loan_amount * pmi_rate) / YEAR_MONTH

        # Calling table header
        make_table_header()
        # initialising some variables to keep track of the entries in the table.
        initial_payment = 0
        total_interest = 0
        total_pmi = 0
        total_principal_paid = 0
        principal_balance = loan_amount
        # Printing first column of the table
        print(f"{initial_payment:>4,}  {principal_balance:>56,.2f} ")

        for payment_number in range(1, loan_term * YEAR_MONTH + 1):
            
            interest_payment = principal_balance * (rate_dict.rates[loan_type] / 100) / YEAR_MONTH
            principal_payment = monthly_payment - interest_payment


            if principal_balance > (0.80 * purchase_price):
                # PMI needs to be applied
                current_pmi_payment = pmi_payment
            else:
                # PMI stops applying
                current_pmi_payment = 0.0

            principal_balance -= principal_payment

            
            # Updating totals
            total_interest += interest_payment
            if (principal_payment >= 0):
                total_principal_paid += principal_payment
            total_pmi += current_pmi_payment
            
            # principal_payment = round(principal_payment,2)
            # principal_balance = round(principal_balance,2)
            # Print each payment row
            print(f"{payment_number:>4,} {interest_payment:>16,.2f} {principal_payment:>19,.2f} {principal_balance:>20,.2f} {current_pmi_payment:>15,.2f}")

            
        # Mortgage Summary
        print("==============================================================================")
        print("\n")
        print(f"Mortgage Summary")
        print(f"Total interest paid: ${total_interest:>56,.2f}")
        print(f"Total payment to principal: ${total_principal_paid:>49,.2f}")
        print(f"Total PMI paid: ${total_pmi:61,.2f}")
        print(f"Total payments: ${total_interest + total_principal_paid + total_pmi:61,.2f}")



    except ValueError:
        print("Invalid input. Please enter numeric values for loan amount, loan term, and interest rate.")

if __name__ == '__main__':
    main()
