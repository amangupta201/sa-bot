import pandas as pd

# Load the CSV file
file_path = r'C:\Users\theam\Downloads\urbanwomania (4).csv'
data = pd.read_csv(file_path)

# Clean and preprocess the data
data['Price'] = data['woocommerce-Price-amount 2'].str.replace(',', '').astype(float)
data['Title'] = data['wd-entities-title']
data['Original Price'] = data['woocommerce-Price-amount'].str.replace(',', '').astype(float)
data['Fabric'] = data.get('Fabric', 'Unknown')  # Assuming 'Fabric' column exists
data['Work Type'] = data.get('Work Type', 'Unknown')  # Assuming 'Work Type' column exists
data = data[['Title', 'Price', 'Original Price', 'out-of-stock', 'Fabric', 'Work Type']]


def get_color_preference():
    colors = input(
        "What color saree do you want? You can specify multiple colors separated by commas: ").strip().lower()
    color_list = [color.strip() for color in colors.split(',') if color.strip()]
    if not color_list:
        print("Please enter at least one valid color.")
        return get_color_preference()
    return color_list


def get_price_range():
    price_range = input("What price range are you looking for? (e.g., 5000-10000) ").strip()
    try:
        min_price, max_price = map(float, price_range.split('-'))
        return min_price, max_price
    except ValueError:
        print("Please enter a valid price range in the format 'min-max'.")
        return get_price_range()


def get_sorting_preference():
    sorting = input(
        "How would you like to sort the results? Enter 'asc' for ascending price or 'desc' for descending price: ").strip().lower()
    if sorting not in ['asc', 'desc']:
        print("Please enter a valid sorting option ('asc' or 'desc').")
        return get_sorting_preference()
    return sorting


def get_fabric_preference():
    fabric = input(
        "Do you have any preference for fabric type? If yes, specify (e.g., silk, cotton) or type 'any' for no preference: ").strip().lower()
    return fabric


def get_work_type_preference():
    work_type = input(
        "Do you have any preference for work type? If yes, specify (e.g., embroidery, print) or type 'any' for no preference: ").strip().lower()
    return work_type


def display_recommendations(recommendations):
    page_size = 5
    total_pages = (len(recommendations) // page_size) + (1 if len(recommendations) % page_size != 0 else 0)

    for page in range(total_pages):
        start_idx = page * page_size
        end_idx = start_idx + page_size
        print(f"\nShowing page {page + 1} of {total_pages}")

        for idx, row in recommendations.iloc[start_idx:end_idx].iterrows():
            stock_status = "In stock" if pd.isna(row['out-of-stock']) else "Out of stock"
            discount = row['Original Price'] - row['Price']
            discount_info = f" (Discount: {discount} off)" if discount > 0 else ""
            print(f"Title: {row['Title']}, Price: {row['Price']}{discount_info}, Stock Status: {stock_status}")
            print(f"Fabric: {row['Fabric']}, Work Type: {row['Work Type']}")
            # Generate URL based on the title
            url_title = row['Title'].replace(' ', '-').lower()
            url = f"https://www.urbanwomania.com/product/{url_title}/"
            print(f"URL: {url}\n")

        if page < total_pages - 1:
            cont = input("Type 'n' to see the next page or anything else to stop: ").strip().lower()
            if cont != 'n':
                break


def get_detailed_feedback():
    feedback = input("Please provide detailed feedback on why the recommendations were helpful or not: ").strip()
    return feedback


def saree_chatbot():
    print("Welcome to the Saree Chatbot!")

    # Get user preferences
    colors = get_color_preference()
    min_price, max_price = get_price_range()
    sorting = get_sorting_preference()
    fabric_preference = get_fabric_preference()
    work_type_preference = get_work_type_preference()

    # Filter data based on user preferences
    recommendations = data[data['Title'].str.lower().str.contains('|'.join(colors)) &
                           (data['Price'] >= min_price) &
                           (data['Price'] <= max_price)]

    # Apply fabric and work type preferences
    if fabric_preference != 'any':
        recommendations = recommendations[recommendations['Fabric'].str.lower().str.contains(fabric_preference)]
    if work_type_preference != 'any':
        recommendations = recommendations[recommendations['Work Type'].str.lower().str.contains(work_type_preference)]

    # Sort the results based on price
    recommendations = recommendations.sort_values(by='Price', ascending=(sorting == 'asc'))

    # Remove duplicate recommendations
    recommendations = recommendations.drop_duplicates(subset=['Title', 'Price'])

    # Check if there are any recommendations
    if not recommendations.empty:
        print("\nHere are some sarees that match your preferences:")
        display_recommendations(recommendations)

        # Get user feedback
        feedback = get_detailed_feedback()
        print(f"Thank you for your feedback: {feedback}")
    else:
        print("Sorry, no sarees match your preferences.")


# Run the chatbot
saree_chatbot()
