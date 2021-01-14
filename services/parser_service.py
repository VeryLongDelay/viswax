from bs4 import BeautifulSoup
import re
import datetime
class ParserService:

    @staticmethod
    def format_table_header_column(th):
        """
        Parses a raw HTML table header column and returns formatted string

        @Params:
        th (string): TableHeader column from countries table

        @Returns:
        Table header as string
        """

        header = " ".join(th.strings)  # join strings broken by <br> tags
        # replace non-breaking space with space and remove \n
        header = header.replace(u"\xa0", u" ").replace("\n", "")
        return header.replace(", ", "/")

    @staticmethod
    def retrieve_viswax_details_from_source(raw_data, tiamat_data):
        """
        Parses the raw HTML response from Worldometer and returns a DataFrame from it

        @Params:
        raw_data (string): request.text from Worldometer

        @Returns:
        Dict
        """

        soup = BeautifulSoup(raw_data, features="html.parser")

        spans = soup.find("span", {"class": "forum-post__body"})
        spans_list = [tag for tag in spans if tag.name!="br"]
        # items of note: 11, 14, 20, 24, 27
        date_of_recipe = spans.find("u").text

        runes = spans.find_all("div", {"class": "bb bb-gold", "style":"display:inline;color:gold"})
        runes_list = list(runes)
        rune_indices = [spans_list.index(x) + 1 for x in runes_list]

        first_rune = spans_list[rune_indices[0]]

        second_runes = spans_list[rune_indices[1]:rune_indices[2]-1]

        date_edited = soup.find("p", {"class": "forum-post__time-below"}).text.split("\n")[1].split(" ")
        date_time_edited = f"{date_edited[4]} {date_edited[5]}"
        date = datetime.datetime.strptime(date_time_edited, '%d-%b-%Y %H:%M:%S')

        vw_fc = {}
        vw_fc['date'] = int(date.timestamp())
        vw_fc['vis_slot_1'] = first_rune
        vw_fc['vis_slot_2'] = second_runes

        soup = BeautifulSoup(tiamat_data, 'html.parser')
        forum_post = soup.find("span", class_="forum-post__body")
        # print(f"{forum_post=}")

        results = []
        for string in forum_post.stripped_strings:
            results.append(string)

        # print(results[3:])

        # strip the header
        results = results[3:]
        vis_date = results[0]

        vis_date = vis_date.replace('Combination for ', '')[:-2]

        pos_slot_1 = results.index('Slot 1:')
        pos_slot_2 = results.index('Slot 2:')
        pos_slot_3 = results.index('Slot 3')

        vis_slot_1 = results[pos_slot_1 + 1:pos_slot_2]
        vis_slot_2 = results[pos_slot_2 + 1:pos_slot_3]

        vis_slot_1[0] = vis_slot_1[0].replace('- ', '')
        vis_2_temp = []
        for item in vis_slot_2:
            vis_2_temp.append(item.replace('- ', '').replace('( ', '(').replace(' )', ')').replace('*', ''))
        vis_slot_2 = []
        for item in vis_2_temp:
            temp_items = item.split(" ")

            new_item = []
            for temp_item in temp_items:
                if '(' in temp_item:
                    item_name = temp_item.replace('(', '')
                    new_item.append(f"({item_name.title()}")
                else:
                    new_item.append(temp_item.title())
            vis_slot_2.append(' '.join(new_item))


        date_edited = soup.find("p", {"class": "forum-post__time-below"}).text.split("\n")[1].split(" ")
        date_time_edited = f"{date_edited[4]} {date_edited[5]}"
        date = datetime.datetime.strptime(date_time_edited, '%d-%b-%Y %H:%M:%S')

        vw_alt = {}
        vw_alt['date'] = int(date.timestamp())
        vw_alt['vis_slot_1'] = vis_slot_1[0]
        vw_alt['vis_slot_2'] = vis_slot_2

        vw = {}
        vw['75-76-378-66118165'] = vw_fc
        vw['75-76-331-66006366'] = vw_alt

        return vw
