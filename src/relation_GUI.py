from relation_GUI_constants import *
import tkinter as tk
from tkinter import messagebox
from idlelib.tooltip import Hovertip
from relation import Rel
from relation import get_FD_string
from relation import get_list_string
from set_theory import Set


def initialise_grid(window):
    """ Creates a grid to hold widgets in a given window.
    Resizes to fit the window.

    Parameters:
        window(Window): the tkinter window

    Returns:
        (Frame): the frame containing the grid
    """
    frame = tk.Frame(window)
    window.rowconfigure(0, weight=DEFAULT_WEIGHT)
    window.columnconfigure(0, weight=DEFAULT_WEIGHT)
    frame.grid(row=0, column=0, sticky='news')
    return frame


def set_cell_weights(frame, num_rows, num_cols):
    """ Sets the weights of rows and columns in the given frame

    Parameters:
        frame(Frame): the frame containing window widgets
        num_rows(int): the number of rows in the frame
        num_cols(int): the number of columns in the frame
    """
    # Set row weights
    for row in range(num_rows):
        if row == LABEL_ROW or row == LABEL_TWO_ROW:
            frame.rowconfigure(row, weight=LABEL_WEIGHT)
        elif row == BODY_ROW or row == BODY_TWO_ROW:
            if row == BODY_ROW and num_rows == EXTENSIVE_NUM_ROWS:
                # Standard label
                frame.rowconfigure(row, weight=LABEL_WEIGHT)
            else:
                frame.rowconfigure(row, weight=BODY_WEIGHT)
        else:
            # Use default weight
            frame.rowconfigure(row, weight=DEFAULT_WEIGHT)
    # Set column weights to default
    for col in range(num_cols):
        frame.columnconfigure(col, weight=DEFAULT_WEIGHT)


class WindowMenu(object):
    """ A class representing the menu of the main window"""

    def __init__(self, parent):
        """ Creates a new WindowMenu instance with a given
        parent window. Provides options to create a new relation
        and to perform calculations.

        Parameters:
            parent(MainWindow): the parent window
        """
        self._parent = parent
        parent_window = parent.get_window()
        menubar = tk.Menu(parent_window)
        # Add option to create new relation
        menubar.add_cascade(
            label='Create relation',
            command=self.create_relation
        )
        # Add submenu to calculate results
        calculate_menu = tk.Menu(menubar, tearoff=0)
        # Add closure option
        calculate_menu.add_command(
            label='closure',
            command=self.get_closure
        )
        # Add superkey option
        calculate_menu.add_command(
            label='superkey test',
            command=self.superkey_test
        )
        # Add candidate key option
        calculate_menu.add_command(
            label='candidate keys',
            command=self.get_keys
        )
        # Add minimal cover option
        calculate_menu.add_command(
            label='minimal cover',
            command=self.compute_cover
        )
        # Add highest normal form option
        calculate_menu.add_command(
            label='highest normal form',
            command=self.highest_NF
        )
        # Add 3NF synthesis option
        calculate_menu.add_command(
            label='3NF synthesis',
            command=self.three_NF_synthesis
        )
        # Add BCNF decomposition option
        calculate_menu.add_command(
            label='BCNF decomposition',
            command=self.BCNF_decomposition
        )
        # Add calculate submenu to menubar
        menubar.add_cascade(
            label='Calculate results',
            menu=calculate_menu
        )
        parent_window.config(menu=menubar)

    def no_relation_message(self):
        """ Creates a message which prompts the
        user to create a relation."""
        messagebox.showinfo(
            'Error',
            'Please create a relation first.'
        )

    def create_relation(self):
        """ Opens a TopLevel window to create a new relation"""
        # Open new window to create relation
        CreateRelationWindow(self._parent)

    def get_closure(self):
        """ Opens a TopLevel window which allows the user
        to calculate the closure of a set"""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Open closure window
            ClosureWindow(self._parent)

    def superkey_test(self):
        """ Opens a TopLevel window which allows the user
        to determine whether a given set is a super key"""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Open superkey window
            SuperKeyWindow(self._parent)

    def get_keys(self):
        """ Opens a TopLevel window which informs the user
        of the candidate keys for the relation"""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Show candidate keys
            CandidateKeysWindow(self._parent)

    def compute_cover(self):
        """ Opens a TopLevel window which computes the
        minimal cover for a given relation. Provides an
        option to compute with union."""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Show minimal cover
            MinimalCoverWindow(self._parent)

    def highest_NF(self):
        """ Opens a TopLevel window which informs the user
        of the highest normal form of the relation.
        Also depicts the first violation instance and cause.
        """
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Show highest normal form
            NormalFormWindow(self._parent)

    def three_NF_synthesis(self):
        """ Opens a TopLevel window which informs the user
        of the 3NF synthesis of the relation."""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Show 3NF synthesis
            ThreeNFWindow(self._parent)

    def BCNF_decomposition(self):
        """ Opens a TopLevel window which informs the user
        of the BCNF decomposition of the relation."""
        if not self._parent.relation_exists():
            # No relation created yet
            self.no_relation_message()
        else:
            # Show BCNF decomposition
            BCNFWindow(self._parent)


class MainWindow(object):
    """ A class representing the main window of the application"""

    def __init__(self):
        """ Creates a new MainWindow instance with which the user
        can create and interact with a relation and its dependencies.
        Application terminates on closure."""
        # Set primary window
        self._main_window = tk.Tk()
        self._main_window.title("Relation Tool")
        # Get monitor size
        screen_width = self._main_window.winfo_screenwidth()
        screen_height = self._main_window.winfo_screenheight()
        # Set main window size
        main_window_width = int(MAIN_WIDTH_SCALE * screen_width)
        main_window_height = int(MAIN_HEIGHT_SCALE * screen_height)
        self._main_window.geometry(
            f'{main_window_width}x{main_window_height}'
        )
        # Configure grid
        self._main_frame = initialise_grid(self._main_window)
        # Initialise relation variable
        self._relation = None
        # Add menubar
        WindowMenu(self)
        # Create loop
        self._main_window.mainloop()

    def get_window(self):
        """ Returns the window representing the application container

        Returns:
            (Window): the tkinter window
        """
        return self._main_window

    def get_frame(self):
        """ Returns the frame in which tkinter widgets can be added

        Returns:
            (Frame): the tkinter frame
        """
        return self._main_frame

    def relation_exists(self):
        """ Determines whether a relation has been created yet

        Returns:
            (bool): True iff a relation has been initialised.
            False otherwise.
        """
        if self._relation is None:
            return False
        return True

    def get_relation(self):
        """ Returns the relation created by the user

        Returns:
            (Rel): the created relation
        """
        return self._relation

    def create_relation(self, attributes):
        """ Creates a new relation with the given attributes

        Parameters:
            attributes(list<str>): the list of attributes
        """
        self._relation = Rel(*attributes)

    def get_width(self, scale):
        """ Returns the width of a widget relative to the
        width of the window.

        Parameters:
            scale(float): the scale of the widget width
                relative to the window

        Returns:
            (int): the width of a widget with given scale
        """
        window_width = self._main_window.winfo_width()
        return int(scale * window_width)

    def get_height(self, scale):
        """ Returns the height of a widget relative to the
        height of the window.

        Parameters:
            scale(float): the scale of the widget height
                relative to the window

        Returns:
            (int): the height of a widget with given scale
        """
        window_height = self._main_window.winfo_height()
        return int(scale * window_height)

    def get_font(self):
        """ Returns the default text font to be used in the
        application, relative to the size of the window.

        Returns:
            (tuple<str, int>): the font tuple
        """
        font_size = self.get_width(FONT_SCALE)
        return ('Arial bold', font_size)

    def clear_widgets(self):
        """ Clears all widgets currently held in the window"""
        for widget in self._main_frame.winfo_children():
            widget.destroy()

    def get_widgets(self):
        """ Returns a list of widgets held in the window

        Returns:
            (list<Widget>): the list of current widgets
        """
        return self._main_frame.winfo_children()


class ChildWindow(object):
    """ An abstract class representing a child window in the application"""

    def __init__(self, parent):
        """ Creates a new ChildWindow instance which is sized relative
        to the main window. The main window cannot be interacted with until
        the child window is closed.

        Parameters:
            parent(MainWindow): the main window
        """
        self._parent = parent
        parent_window = parent.get_window()
        self._child_window = tk.Toplevel(parent_window)
        self._child_window.grab_set()  # Set focus
        self._child_window.wm_transient(parent_window)  # Bring to foreground
        # Calculate child dimensions
        child_width = parent.get_width(CHILD_WIDTH_SCALE)
        child_height = parent.get_height(CHILD_HEIGHT_SCALE)
        # Get parent offset
        offset_x = parent_window.winfo_rootx()
        offset_y = parent_window.winfo_rooty()
        # Set child dimensions
        self._child_window.geometry(
            f'{child_width}x{child_height}'
            f'+{offset_x + child_width // 2}'
            f'+{offset_y + child_height // 2}'
        )
        # Update the geometry of child window
        self._child_window.update_idletasks()
        # Configure grid
        self._child_frame = initialise_grid(self._child_window)

    def get_parent(self):
        """ Returns the main window instance

        Returns:
            (MainWindow): the main window
        """
        return self._parent

    def get_window(self):
        """ Returns the window representing the child container

        Returns:
            (Window): the tkinter window
        """
        return self._child_window

    def get_frame(self):
        """ Returns the frame in which tkinter widgets can be added

        Returns:
            (Frame): the tkinter frame
        """
        return self._child_frame

    def get_width(self, scale):
        """ Returns the width of a widget relative to the
        width of the window.

        Parameters:
            scale(float): the scale of the widget width
                relative to the window

        Returns:
            (int): the width of a widget with given scale
        """
        child_width = self._child_window.winfo_width()
        return int(scale * child_width)

    def get_height(self, scale):
        """ Returns the height of a widget relative to the
        height of the window.

        Parameters:
            scale(float): the scale of the widget height
                relative to the window

        Returns:
            (int): the height of a widget with given scale
        """
        window_height = self._child_window.winfo_height()
        return int(scale * window_height)

    def get_font(self):
        """ Returns the default text font to be used in the
        application, relative to the size of the window.

        Returns:
            (tuple<str, int>): the default font tuple
        """
        font_size = self.get_width(FONT_SCALE)
        return ('Arial bold', font_size)

    def get_title_font(self):
        """ Returns the text font for titles to be used in the
        application, relative to the size of the window.

        Returns:
            (tuple<str, int>): the title font tuple
        """
        font_size = self.get_width(TITLE_FONT_SCALE)
        return ('Arial bold', font_size)

    def get_button_font(self):
        """ Returns the text font for buttons to be used in the
        application, relative to the size of the window.

        Returns:
            (tuple<str, int>): the button font tuple
        """
        font_size = self.get_width(BUTTON_FONT_SCALE)
        return ('Arial', font_size)


class CreateRelationWindow(ChildWindow):
    """ A class representing a window used to create new relations,
    which extends ChildWindow."""

    def __init__(self, parent):
        """ Creates a new CreateRelationWindow instance and lays
        out the widgets therein.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent)
        # Create label
        LabelText(
            self,
            'Please enter attributes in the box below.\n'
            'Enter attributes on each new line.',
            LABEL_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create scrolled text to enter attributes
        self._text = ScrolledHVText(
            self,
            True,
            True,
            BODY_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Enable text for editing
        self._text.enable_text()
        # Create cancel button
        CancelButton(
            self,
            BUTTON_ROW,
            CANCEL_BUTTON_COL
        )
        # Create submit button
        CreateRelationButton(
            self,
            BUTTON_ROW,
            SUBMIT_BUTTON_COL
        )
        # Set cell weights
        set_cell_weights(
            self._child_frame,
            DEFAULT_NUM_ROWS,
            DEFAULT_NUM_COLS
        )

    def get_attributes(self):
        """ Determines the list of attributes specified
        by the user in the text field. Removes whitespace,
        and ignores blank string and any duplicates.

        Returns:
            (list<str>): the list of attributes
        """
        attribute_text = self._text.get_text('1.0', tk.END)
        raw_attributes = attribute_text.split('\n')
        attributes = []
        for index, attribute in enumerate(raw_attributes):
            # Remove white space
            raw_attributes[index] = attribute.strip()
        for attribute in raw_attributes:
            # Ignore empty strings and duplicates
            if len(attribute) != 0 and attribute not in attributes:
                attributes.append(attribute)
        return attributes


class CreateDependencyWindow(ChildWindow):
    """ A class representing a window used to create new dependencies,
    which extends ChildWindow."""

    def __init__(self, parent):
        """ Creates a new CreateDependencyWindow instance and lays
        out the widgets therein.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent)
        # Create dependency label
        self._dependency_label = ScrolledHVText(
            self,
            True,
            False,
            LABEL_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Get list of attributes
        attributes = parent.get_relation().attributes_list()
        # Create left list of attributes
        self._left_list = ScrolledListbox(
            self,
            BODY_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN // 2
        )
        # Add attributes to left list
        self._left_list.add_lines(attributes)
        # Bind list event handler to left list
        self._left_list.bind(self.list_event_handler)
        # Create right list of attributes
        self._right_list = ScrolledListbox(
            self,
            BODY_ROW,
            RIGHT_TEXT_COL,
            DEFAULT_COL_SPAN // 2
        )
        # Add attributes to right list
        self._right_list.add_lines(attributes)
        # Bind list event handler to right list
        self._right_list.bind(self.list_event_handler)
        # Initialise dependency label text
        self.set_dependency_text()
        # Create cancel button
        CancelButton(
            self,
            BUTTON_ROW,
            CANCEL_BUTTON_COL
        )
        # Create submit button
        CreateDependencyButton(
            self,
            BUTTON_ROW,
            SUBMIT_BUTTON_COL
        )
        # Add blank buttons to maintain proportions
        BlankButton(
            self,
            BUTTON_ROW,
            BLANK_BUTTON_ONE_COL
        )
        BlankButton(
            self,
            BUTTON_ROW,
            BLANK_BUTTON_TWO_COL
        )
        # Set cell weights
        set_cell_weights(
            self._child_frame,
            DEFAULT_NUM_ROWS,
            DEFAULT_NUM_COLS
        )

    def is_dependency_empty(self):
        """ Determines whether the given dependency
        contains at least one attribute on both sides.

        Returns:
            (bool): True iff the dependency has at least
            one attribute on both sides. False otherwise.
        """
        return self.get_left_attributes() == [] \
            or self.get_right_attributes() == []

    def get_left_attributes(self):
        """ Returns a list of which attributes the
        user has selected on the left-hand side.

        Returns:
            (list<str>): the list of selected attributes
        """
        return self._left_list.get_selected_lines()

    def get_right_attributes(self):
        """ Returns a list of which attributes the
        user has selected on the right-hand side.

        Returns:
            (list<str>): the list of selected attributes
        """
        return self._right_list.get_selected_lines()

    def list_event_handler(self, event):
        """ Handles the current event for the given listbox.
        Sets the dependency text whenever the user updates
        their selection in the given listbox.

        Parameters:
            event(ListboxSelect): the event
        """
        self.set_dependency_text()

    def set_dependency_text(self):
        """ Sets the dependency text in the dependency label
        widget, based on the left- and right-hand attributes
        currently selected by the user."""
        left_attributes = self.get_left_attributes()
        right_attributes = self.get_right_attributes()
        self._dependency_label.set_text(
            get_FD_string(left_attributes, right_attributes)
        )


class NormalFormWindow(ChildWindow):
    """ A class representing a window used to determine the highest
    normal form and any reason(s) for violation.
    Extends ChildWindow."""

    def __init__(self, parent):
        """ Creates a new NormalFormWindow instance and lays
        out the widgets therein.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent)
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Create title
        TitleText(
            self,
            'Highest normal form',
            LABEL_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create normal form text
        text_one = ScrolledHVText(
            self,
            True,
            False,
            BODY_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Set normal form text
        text_one.set_text(f' {relation.highest_NF()}')
        # Create label
        LabelText(
            self,
            'First cause of violation:',
            LABEL_TWO_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create reason text
        text_two = ScrolledHVText(
            self,
            True,
            True,
            BODY_TWO_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Set reason text
        text_two.set_text(self.get_reason())
        # Create okay button
        OkayButton(
            self,
            BUTTON_TWO_ROW,
            SUBMIT_BUTTON_COL
        )
        # Set cell weights
        set_cell_weights(
            self._child_frame,
            EXTENSIVE_NUM_ROWS,
            DEFAULT_NUM_COLS
        )

    def get_reason(self):
        """ Returns a string detailing which dependency resulted
        in a normal form violation, and the reason(s) therefore.
        In the case where the relation is in BCNF, a string
        specifying that no violation was found is returned instead.

        Returns:
            (str): the string detailing the problem dependency (if any)
            and the reason(s) for the violation.
        """
        # Get relation from parent
        parent = self.get_parent()
        relation = parent.get_relation()
        # Find highest normal form
        normal_form = relation.highest_NF()
        # Get widget which holds dependencies
        for widget in parent.get_widgets():
            if isinstance(widget, tk.Listbox):
                # Found it
                break
        if normal_form == '1NF':
            # Highest normal form is 1NF
            index, subset, key, attribute = relation.two_NF(True)
            reason = f' {BULLET} {subset} is a proper subset of key {key}\n' \
                     f' {BULLET} {attribute} is not a prime attribute'
        elif normal_form == '2NF':
            # Highest normal form is 2NF
            index, subset, attribute = relation.three_NF(True)
            reason = f' {BULLET} {subset} is not a superkey\n' \
                     f' {BULLET} {attribute} is not a prime attribute'
        elif normal_form == '3NF':
            # Highest normal form is 3NF
            index, subset = relation.BCNF(True)
            reason = f' {BULLET} {subset} is not a superkey'
        else:
            # Highest normal form is BCNF
            return ' No violations found'
        # Highest normal form is not BCNF
        dependency = widget.get(index)
        return f' Dependency\n{dependency}\n\n{reason}'


class OutputWindow(ChildWindow):
    """ An abstract class representing a window which outputs the result
    of a given calculation. Extends ChildWindow."""

    def __init__(self, parent, title):
        """ Creates a new OutputWindow instance and lays
        out the widgets therein.

        Parameters:
            parent(MainWindow): the main window
            title(str): the text used for the window title
        """
        super().__init__(parent)
        # Create title
        TitleText(
            self,
            title,
            LABEL_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create scrolled text
        self._text = ScrolledHVText(
            self,
            True,
            True,
            BODY_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create okay button
        OkayButton(
            self,
            BUTTON_ROW,
            SUBMIT_BUTTON_COL
        )
        # Set cell weights
        set_cell_weights(
            self._child_frame,
            DEFAULT_NUM_ROWS,
            DEFAULT_NUM_COLS
        )


class CandidateKeysWindow(OutputWindow):
    """ A class representing a window which outputs any
    candidate keys found for the relation, which extends
    OutputWindow."""

    def __init__(self, parent):
        """ Creates a new CandidateKeysWindow instance and lays
        out the widgets therein, setting the candidate
        keys text in the process.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, 'Candidate keys')
        # Set scrolled text to contain keys
        self._text.set_text(self.get_keys())

    def get_keys(self):
        """ Returns the string of candidate keys for the
        relation.

        Returns:
            (str): the candidate keys for the relation
        """
        keys_string = ''
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Get candidate keys set
        keys_set = relation.keys()
        # Iterate through keys set and add to string
        for index, key_set in enumerate(keys_set.elements(), 1):
            if index != 1:
                # Append newline character
                keys_string += '\n'
            # Append key number to string
            keys_string += f'{f"{index}. ":>4}'
            # Append key to string
            keys_string += get_list_string(key_set.elements())
        return keys_string


class MinimalCoverWindow(OutputWindow):
    """ A class representing a window which outputs the
    minimal cover for the relation, which extends
    OutputWindow."""

    def __init__(self, parent):
        """ Creates a new MinimalCoverWindow instance and lays
        out the widgets therein, setting the min cover text.
        Provides a button to toggle union on and off.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, 'Minimal cover')
        # Set min cover text
        self.set_min_cover_text()
        # Create union button
        UnionButton(
            self,
            BUTTON_ROW,
            LEFT_TEXT_COL
        )

    def set_min_cover_text(self, union=None):
        """ Sets the minimal cover for the relation.
        If union == True, then the set text is the
        minimal cover with union.

        Parameters:
            union(bool): an option to use the union
                of the minimal cover
        """
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Get minimal cover
        min_dependencies = relation.min_cover(union).get_dependencies()
        # Set minimal cover text
        self._text.set_text(min_dependencies)


class ThreeNFWindow(OutputWindow):
    """ A class representing a window which outputs the
    3NF synthesis for the relation, which extends
    OutputWindow."""

    def __init__(self, parent):
        """ Creates a new ThreeNFWindow instance and lays out
        the widgets therein, setting the 3NF synthesis text.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, '3NF synthesis')
        # Set 3NF synthesis text
        self._text.set_text(self.get_three_NF_text())

    def get_three_NF_text(self):
        """ Returns a string containing the 3NF synthesis
        of the relation.
        
        Returns:
            (str): the 3NF synthesis of the relation
        """
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Get 3NF synthesis
        three_NF_text = relation.three_NF_decomp()
        return three_NF_text


class BCNFWindow(OutputWindow):
    """ A class representing a window which outputs the
    BCNF decomposition for the relation, which extends
    OutputWindow."""

    def __init__(self, parent):
        """ Creates a new BCNFWindow instance and lays out
        the widgets therein, setting the BCNF decomposition text.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, 'BCNF decomposition')
        # Set BCNF decomposition text
        self._text.set_text(self.get_BCNF_text())

    def get_BCNF_text(self):
        """ Returns a string containing the BCNF decomposition
        of the relation.
        
        Returns:
            (str): the BCNF decomposition of the relation
        """
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Get BCNF decomposition
        BCNF_text = relation.BCNF_decomp()
        return BCNF_text


class OptionWindow(ChildWindow):
    """ An abstract class representing a window which provides options
    to the user when performing calculations. Extends ChildWindow."""

    def __init__(self, parent, title):
        """ Creates a new OptionWindow instance and lays
        out the widgets therein.

        Parameters:
            parent(MainWindow): the main window
            title(str): the text used for the window title
        """
        super().__init__(parent)
        # Get relation from parent
        relation = self.get_parent().get_relation()
        # Create title
        TitleText(
            self,
            title,
            LABEL_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create set text
        self._text_one = ScrolledHVText(
            self,
            True,
            False,
            BODY_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create output text
        self._text_two = ScrolledHVText(
            self,
            True,
            False,
            LABEL_TWO_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Create list of attributes
        self._list = ScrolledListbox(
            self,
            BODY_TWO_ROW,
            LEFT_TEXT_COL,
            DEFAULT_COL_SPAN
        )
        # Get list of attributes
        attributes = parent.get_relation().attributes_list()
        # Add attributes to list
        self._list.add_lines(attributes)
        # Bind list event handler to left list
        self._list.bind(self.list_event_handler)
        # Initialise set label text
        self.set_attributes_text()
        # Create okay button
        OkayButton(
            self,
            BUTTON_TWO_ROW,
            SUBMIT_BUTTON_COL
        )
        # Set cell weights
        set_cell_weights(
            self._child_frame,
            EXTENSIVE_NUM_ROWS,
            DEFAULT_NUM_COLS
        )

    def list_event_handler(self, event):
        """ Handles the current event for the given listbox.
        Sets the attributes text whenever the user updates
        their selection in the given listbox."""
        self.set_attributes_text()

    def set_attributes_text(self):
        """ Sets the text detailing the attributes currently
        selected by the user in the listbox."""
        # Get selected attributes
        attributes_sublist = self._list.get_selected_lines()
        # Find attributes string
        attributes_sublist_string = get_list_string(attributes_sublist)
        self._text_one.set_text(
            f' Set = {attributes_sublist_string}'
        )


class ClosureWindow(OptionWindow):
    """ A class representing a window which outputs the closure
    of the given attributes selected by the user.
    Extends OptionWindow."""

    def __init__(self, parent):
        """ Creates a new ClosureWindow instance and lays out
        the widgets therein, initialising the closure text.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, 'Closure')
        # Initialise closure label text
        self.set_closure_text()

    def list_event_handler(self, event):
        """ Handles the current event for the given listbox.
        Sets the attributes and closure text whenever the
        user updates their selection in the given listbox.

        Parameters:
            event(ListboxSelect): the event
        """
        super().list_event_handler(event)
        self.set_closure_text()

    def set_closure_text(self):
        """ Sets the text detailing the closure of the attributes
        currently selected by the user in the listbox."""
        relation = self.get_parent().get_relation()
        # Get selected attributes and convert to Set
        attributes_subset = Set(*self._list.get_selected_lines())
        # Find closure set
        closure_set = relation.closure(attributes_subset)
        # Find closure string
        closure_string = get_list_string(closure_set.elements())
        self._text_two.set_text(
            f' Closure = {closure_string}'
        )


class SuperKeyWindow(OptionWindow):
    """ A class representing a window which outputs whether the
    given attributes selected by the user forms a super key.
    Extends OptionWindow."""

    def __init__(self, parent):
        """ Creates a new SuperKeyWindow instance and lays out
        the widgets therein, initialising the super key text.

        Parameters:
            parent(MainWindow): the main window
        """
        super().__init__(parent, 'Superkey test')
        # Initialise superkey label text
        self.set_superkey_text()

    def list_event_handler(self, event):
        """ Handles the current event for the given listbox.
        Sets the attributes and closure text whenever the
        user updates their selection in the given listbox.

        Parameters:
            event(ListboxSelect): the event
        """
        super().list_event_handler(event)
        self.set_superkey_text()

    def set_superkey_text(self):
        """ Sets the text detailing whether the attributes
        currently selected by the user in the listbox forms
        a super key."""
        relation = self.get_parent().get_relation()
        # Get selected attributes and convert to Set
        attributes_subset = Set(*self._list.get_selected_lines())
        # Determine whether subset forms a superkey
        is_superkey = relation.super_key(attributes_subset)
        self._text_two.set_text(
            f' Superkey = {is_superkey}'
        )
        if is_superkey:
            # Make text green
            self._text_two.set_text_colour(
                GREEN,
                START_SUPERKEY_COLOUR,
                tk.END
            )
        else:
            # Make text red
            self._text_two.set_text_colour(
                'red',
                START_SUPERKEY_COLOUR,
                tk.END
            )


class WindowComponent(object):
    """ An abstract class representing a custom widget
    in the tkinter window"""

    def __init__(self, relative):
        """ Creates a new WindowComponents instance

        Parameters:
            relative(object): the window in which the
            widget resides, either MainWindow or ChildWindow
        """
        self._relative = relative
        self._frame = relative.get_frame()
        self._window = relative.get_window()


class LabelType(WindowComponent):
    """ An abstract class representing a type of label which
    can be placed in the tkinter window. Extends WindowComponent."""

    def __init__(self, relative, text, row_num, col_num, col_span):
        """ Creates a new LabelType instance and places it in
        the window

        Parameters:
            relative(object): the window in which the label resides
            text(str): the text to be displayed in the label
            row_num(int): the row in which the label resides
            col_num(int): the column in which the label resides
            col_span(int): the number of columns over which the label spans
        """
        super().__init__(relative)
        # Create label
        self._label = tk.Label(
            self._frame,
            justify=tk.LEFT,
            anchor='w',
            text=text
        )
        # Fix label to grid
        self._label.grid(
            column=col_num,
            row=row_num,
            columnspan=col_span,
            sticky='news'
        )


class TitleText(LabelType):
    """ A class representing the title of a window, which extends
    LabelType"""

    def __init__(self, relative, text, row_num, col_num, col_span):
        """ Creates a new TitleText instance and places it in
        the window. Sets the font of the title.

        Parameters:
            relative(object): the window in which the title resides
            text(str): the text to be displayed in the title
            row_num(int): the row in which the title resides
            col_num(int): the column in which the title resides
            col_span(int): the number of columns over which the title spans
        """
        super().__init__(relative, text, row_num, col_num, col_span)
        # Change font of label
        self._label.configure(
            font=self._relative.get_title_font()
        )


class LabelText(LabelType):
    """ A class representing the label of a window, which extends
    LabelType"""

    def __init__(self, relative, text, row_num, col_num, col_span):
        """ Creates a new LabelText instance and places it in
        the window. Sets the font of the label.

        Parameters:
            relative(object): the window in which the label resides
            text(str): the text to be displayed in the label
            row_num(int): the row in which the label resides
            col_num(int): the column in which the label resides
            col_span(int): the number of columns over which the label spans
        """
        super().__init__(relative, text, row_num, col_num, col_span)
        # Change font of label
        self._label.configure(
            font=self._relative.get_font()
        )


class ScrolledHVText(WindowComponent):
    """ A class representing a Text widget, which can be scrolled
    horizontally and vertically. Extends WindowComponent."""

    def __init__(self, relative, horizontal, vertical,
                 row_num, col_num, col_span):
        """ Creates a new ScrolledHVText instance and places it in
        the window. Horizontal and vertical scrollbars can be optionally
        set.

        Parameters:
            relative(object): the window in which the textbox resides
            horizontal(bool): if True, sets a horizontal scroll bar
            vertical(bool): if True, sets a vertical scroll bar
            row_num(int): the row in which the textbox resides
            col_num(int): the column in which the textbox resides
            col_span(int): the number of columns over which the textbox spans
        """
        super().__init__(relative)
        # Create text
        self._text = tk.Text(
            self._frame,
            height=SCROLLED_TEXT_HEIGHT,
            spacing1=TEXT_SPACING,
            font=self._relative.get_font(),
            state=tk.DISABLED,
            wrap=tk.NONE
        )
        # Add text to grid
        self._text.grid(
            column=col_num,
            row=row_num,
            columnspan=col_span,
            sticky='news'
        )
        # Add scrollbars (if specified)
        if horizontal:
            # Add horizontal scrollbar
            text_scroll_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
            self._text.configure(xscrollcommand=text_scroll_x.set)
            text_scroll_x.config(command=self._text.xview)
            # Add scrollbar to grid
            text_scroll_x.grid(
                column=col_num,
                row=row_num + 1,
                columnspan=col_span,
                sticky='new'
            )
        if vertical:
            # Add vertical scrollbar
            text_scroll_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL)
            self._text.configure(yscrollcommand=text_scroll_y.set)
            text_scroll_y.config(command=self._text.yview)
            # Add scrollbar to grid
            text_scroll_y.grid(
                column=col_num + col_span,
                row=row_num,
                sticky='nsw'
            )

    def enable_text(self):
        """ Enables text editing in the widget and sets
        cursor to xterm."""
        self._text.configure(
            state=tk.NORMAL,
            cursor='xterm'
        )

    def disable_text(self):
        """ Disables text editing in the widget and sets
        cursor to default."""
        self._text.configure(
            state=tk.DISABLED,
            cursor='arrow'
        )

    def get_text(self, start, end):
        """ Gets the text currently between the start and end indexes,
        inclusive.

        Parameters:
            start(str): the start index of the text
            end(str): the end index of the text

        Returns:
            (str): the text in the widget
        """
        return self._text.get(start, end)

    def set_text(self, text):
        """ Resets the contents of the widget and sets the text
        with the specified string.

        Parameters:
            text(str): the text to insert into the widget
        """
        # Enable ability to modify text
        self.enable_text()
        # Clear text
        self._text.delete('1.0', tk.END)
        # Insert text
        self._text.insert(tk.INSERT, text)
        # Disable ability to modify text
        self.disable_text()

    def set_text_colour(self, colour, start, end):
        """ Changes the colour of the text in the widget
        between the specified start and end indexes, inclusive.

        Parameters:
            colour(str): the colour of the text
            start(str): the start index of the text
            end(str): the end index of the text
        """
        # Create colour tag
        self._text.tag_add('colour', start, end)
        # Configure tag
        self._text.tag_configure('colour', foreground=colour)


class ScrolledListbox(WindowComponent):
    """ A class representing a Listbox widget, which can be scrolled
    horizontally and vertically. Extends WindowComponent."""

    def __init__(self, relative, row_num, col_num, col_span):
        """ Creates a new ScrolledListbox instance and places it in
        the window.

        Parameters:
            relative(object): the window in which the listbox resides
            row_num(int): the row in which the listbox resides
            col_num(int): the column in which the listbox resides
            col_span(int): the number of columns over which the listbox spans
        """
        super().__init__(relative)
        # Add scrollbar for listbox widget
        listbox_scroll_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL)
        listbox_scroll_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL)
        # Create listbox
        self._listbox = tk.Listbox(
            self._frame,
            height=MIN_NUM_LIST_LINES,
            font=self._relative.get_font(),
            cursor='hand2',
            selectmode=tk.MULTIPLE,
            exportselection=False,
            activestyle=tk.NONE,
            xscrollcommand=listbox_scroll_x.set,
            yscrollcommand=listbox_scroll_y.set
        )
        # Add listbox to grid
        self._listbox.grid(
            column=col_num,
            row=row_num,
            columnspan=col_span,
            sticky='news'
        )
        # Configure scrollbar
        listbox_scroll_x.config(command=self._listbox.xview)
        listbox_scroll_y.config(command=self._listbox.yview)
        # Add scrollbars to grid
        listbox_scroll_x.grid(
            column=col_num,
            row=row_num + 1,
            columnspan=col_span,
            sticky='new'
        )
        listbox_scroll_y.grid(
            column=col_num + col_span,
            row=row_num,
            sticky='nsw'
        )

    def bind(self, function):
        """ Calls the given function whenever there is an update
        in the Listbox selection.

        Parameters:
            function: the function to call
        """
        # Binds function to listbox
        self._listbox.bind('<<ListboxSelect>>', function)

    def get_selected_lines(self):
        """ Returns a list of lines currently selected by the user
        in the Listbox.

        Returns:
            (list<str>): the list of selected lines
        """
        selected_lines = []
        for index in self._listbox.curselection():
            selected_lines.append(self._listbox.get(index))
        return selected_lines

    def add_lines(self, lines):
        """ Adds the list of lines to the end of the Listbox
        as new options.

        Parameters:
            lines(list<str>): the list of lines to add
        """
        self._listbox.insert(tk.END, *lines)

    def remove_lines(self):
        """ Removes any options from the Listbox which are currently
        selected by the user."""
        # Remove currently selected lines
        for index in self._listbox.curselection():
            self._listbox.delete(index)


class BaseButton(WindowComponent):
    """ An abstract class representing a type of button which
    can be placed in the tkinter window. Extends WindowComponent."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new BaseButton instance and places it in
        the window.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative)
        # Create button
        self._button = tk.Button(
            self._frame,
            cursor='hand2',
            command=self.button_action
        )
        # Add button to grid
        self._button.grid(column=col_num, row=row_num, sticky='news')

    def button_action(self):
        """ Represents an abstract function which is called whenever the
        button is pressed."""
        return


class TextButton(BaseButton):
    """ An abstract class representing a type of button which contains text.
    Extends BaseButton."""

    def set_text(self, text):
        """ Sets the given string of text to be displayed by the
        button.

        Parameters:
            text(str): the text to be displayed
        """
        self._button.configure(
            height=BUTTON_TEXT_HEIGHT,
            font=self._relative.get_button_font(),
            text=text
        )


class BlankButton(TextButton):
    """ A class representing a type of button which is not visible.
   Extends TextButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new BlankButton instance and places it in
        the window. Sets the text as 'Blank '.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        self.set_text('Blank ')
        # Hide button from sight
        self._button.configure(
            bd=0,
            state=tk.ACTIVE,
            fg=self._window['bg'],
            activeforeground=self._window['bg']
        )


class CloseButton(TextButton):
    """ An abstract class representing a type of button which closes the
    active window on interaction. Extends TextButton."""

    def button_action(self):
        """ Closes the window on button interaction."""
        # Close window
        self._window.destroy()


class CancelButton(CloseButton):
    """ A class representing a type of button which closes the
    window and displays text. Extends CloseButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new CancelButton instance and places it in
        the window. Sets the text as 'Cancel'.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Set text of cancel button
        self.set_text('Cancel')


class OkayButton(CloseButton):
    """ A class representing a type of button which closes the
    window and displays text. Extends CloseButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new OkayButton instance and places it in
        the window. Sets the text as 'Okay'.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Set text of okay button
        self.set_text('Okay')


class SubmitButton(TextButton):
    """ An abstract class representing a type of button which performs
    an action and closes the window. Extends TextButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new SubmitButton instance and places it in
        the window. Sets the text as 'Submit'.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Set text of submit button
        self.set_text('Submit')


class CreateRelationButton(SubmitButton):
    """ A class representing a type of button which creates a new relation
    and closes the window. Extends SubmitButton."""

    def button_action(self):
        """ Attempts to create a new relation and add components to the
        main window, on button interaction."""
        attributes = self._relative.get_attributes()
        if len(attributes) == 0:
            # No attributes given
            messagebox.showinfo(
                'Error',
                'Please enter at least one attribute.',
                parent=self._relative.get_window()
            )
        else:
            parent = self._relative.get_parent()
            # Create a new relation with given attributes
            parent.create_relation(attributes)
            # Close child window
            self._window.destroy()
            # Destroy any components in the parent window
            parent.clear_widgets()
            # Add relation components to main window
            RelationComponents(parent)


class CreateDependencyButton(SubmitButton):
    """ A class representing a type of button which creates a new dependency
    and closes the window. Extends SubmitButton."""

    def button_action(self):
        """ Attempts to create a new dependency and add it to the
        ScrolledListbox in the main window, on button interaction."""
        child = self._relative
        if child.is_dependency_empty():
            # No attributes selected on left- or right-hand sides
            messagebox.showinfo(
                'Error',
                'Please select attributes on left- and right-hand '
                'sides of dependency.',
                parent=self._relative.get_window()
            )
            return
        # Try creating dependency
        parent = self._relative.get_parent()
        relation = parent.get_relation()
        # Get left and right attributes
        left_attributes = child.get_left_attributes()
        right_attributes = child.get_right_attributes()
        # Check if relation contains dependency in question
        FD_string = get_FD_string(left_attributes, right_attributes)
        if relation.contains_FD(FD_string):
            # Relation already contains dependency
            messagebox.showinfo(
                'Error',
                'Relation already contains the given dependency.',
                parent=self._relative.get_window()
            )
            return
        # Add dependency to relation
        output = relation.add_FD(left_attributes, right_attributes)
        if isinstance(output, ValueError):
            # Dependency must be trivial
            messagebox.showinfo(
                'Error',
                'Please ensure that the dependency is non-trivial.',
                parent=self._relative.get_window()
            )
            return
        # Add dependency to main window list
        for widget in parent.get_widgets():
            if isinstance(widget, tk.Listbox):
                # Add dependency
                widget.insert(
                    tk.END,
                    f' {get_FD_string(left_attributes, right_attributes)}'
                )
                break
        # Close child window
        self._window.destroy()


class UnionButton(TextButton):
    """ A class representing a type of button which enables or disables
    union of the displayed minimal cover. Extends TextButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new UnionButton instance and places it in
        the window. Sets the text as 'Union' and configures visuals.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Set text on union button
        self.set_text(f'Union {OFF}')
        # Configure button options
        self._button.configure(relief=tk.GROOVE)
        # Configure grid options
        self._button.grid(sticky='nes')

    def button_action(self):
        """ Toggles whether to display the minimal cover with union
        or no union, on button interaction."""
        button_text = self._button['text']
        if button_text == f'Union {OFF}':
            # Put button in ON state
            self._button.configure(text=f'Union {ON}')
            # Set min cover text (with union)
            self._relative.set_min_cover_text(True)
        else:
            # Put button in OFF state
            self._button.configure(text=f'Union {OFF}')
            # Set min cover text
            self._relative.set_min_cover_text()


class ImageButton(BaseButton):
    """ An abstract class representing a type of button which displays
    an image and shows a tooltip. Extends BaseButton."""

    def set_image(self, file_name):
        """ Sets the image displayed by the button using the picture
        located at the given filepath.

        Parameters:
            file_name(str): the relative path of the image
        """
        icon = tk.PhotoImage(file=file_name) \
            .subsample(PHOTO_PIXEL_SKIP, PHOTO_PIXEL_SKIP)
        self._button.configure(image=icon)
        self._button.photo = icon

    def set_tooltip(self, text):
        """ Sets a tooltip which displays the specified text.

        Parameters:
            text(str): the text to be displayed by the tooltip
        """
        Hovertip(self._button, text, BUTTON_TIP_DELAY)


class InsertionButton(ImageButton):
    """ A class representing a type of button which shows an icon
    and opens a window to create a new dependency.
    Extends ImageButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new InsertionButton instance and places it in
        the window. Sets the image and tooltip.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Add image to insertion button
        self.set_image('assets/plus_icon.png')
        # Add tooltip to insertion button
        self.set_tooltip('Add a dependency')

    def button_action(self):
        """ Opens a new CreateDependencyWindow instance on button
        interaction."""
        # Open new window to create dependency
        CreateDependencyWindow(self._relative)


class DeletionButton(ImageButton):
    """ A class representing a type of button which shows an icon
    and deletes any selected dependencies.
    Extends ImageButton."""

    def __init__(self, relative, row_num, col_num):
        """ Creates a new DeletionButton instance and places it in
        the window. Sets the image and tooltip.

        Parameters:
            relative(object): the window in which the button resides
            row_num(int): the row in which the button resides
            col_num(int): the column in which the button resides
        """
        super().__init__(relative, row_num, col_num)
        # Add image to deletion button
        self.set_image('assets/trash_icon.png')
        # Add tooltip to deletion button
        self.set_tooltip('Delete selected dependencies')

    def button_action(self):
        """ Deletes the selected dependencies, on button interaction."""
        # Get parent and relation
        parent = self._relative
        relation = parent.get_relation()
        # Remove selected dependencies
        for widget in parent.get_widgets():
            if isinstance(widget, tk.Listbox):
                # Found the listbox
                break
        for dependency in widget.curselection()[::-1]:
            # Work backwards
            # Remove dependency from relation
            relation.remove_FD(dependency + 1)
            # Remove dependency from screen
            widget.delete(dependency)


class RelationComponents(WindowComponent):
    """ A class which adds GUI components to the MainWindow when
    a new relation is created. Extends WindowComponent."""

    def __init__(self, relative):
        """ Adds components to display the current relation, and its dependencies.
        Buttons are added which enable insertion and deletion of dependencies.

        Parameters:
            relative(object): the window to which the components are added
        """
        super().__init__(relative)
        # Create relation label
        relation_label = ScrolledHVText(
            self._relative,
            True,
            False,
            LABEL_ROW,
            LEFT_TEXT_COL,
            EXTENSIVE_COL_SPAN
        )
        # Set relation text
        relation = self._relative.get_relation()
        relation_label.set_text(
            f' {relation.get_relation()}'
        )
        # Create list of dependencies
        ScrolledListbox(
            self._relative,
            BODY_ROW,
            LEFT_TEXT_COL,
            EXTENSIVE_COL_SPAN
        )
        # Create dependency insertion button
        InsertionButton(
            self._relative,
            BUTTON_ROW,
            INSERTION_BUTTON_COL
        )
        # Create dependency deletion button
        DeletionButton(
            self._relative,
            BUTTON_ROW,
            DELETION_BUTTON_COL
        )
        # Set cell weights
        set_cell_weights(
            self._frame,
            DEFAULT_NUM_ROWS,
            EXTENSIVE_NUM_COLS
        )


def main():
    """ Opens a tkinter application which handles all interaction
    with the user."""
    # Initialise application
    MainWindow()


if __name__ == "__main__":
    main()
