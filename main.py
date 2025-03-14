import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, NumericProperty
from kivy.graphics import Color, Rectangle

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    # Input row for adding a task
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        TextInput:
            id: task_input
            hint_text: "Task"
        TextInput:
            id: due_input
            hint_text: "Due (days)"
            input_filter: 'int'
        TextInput:
            id: diff_input
            hint_text: "Difficulty (1-5)"
            input_filter: 'int'
        Button:
            text: "Add"
            on_release: app.add_task(task_input.text, due_input.text, diff_input.text)
    
    # RecycleView to display tasks with selection capability
    RecycleView:
        id: rv
        viewclass: "SelectableLabel"
        RecycleBoxLayout:
            default_size: None, dp(40)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

    # Buttons for removing and sorting tasks
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 10
        Button:
            text: "Remove Task"
            on_release: app.remove_task()
        Button:
            text: "Sort by Priority"
            on_release: app.sort_tasks()
'''

class SelectableLabel(RecycleDataViewBehavior, Label):
    index = NumericProperty(0)
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)  # default unselected background: black
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect, selected=self.update_color)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_color(self, instance, value):
        # Change background color based on selection
        if self.selected:
            self.bg_color.rgba = (0.6, 0.6, 0.6, 1)  # gray when selected
        else:
            self.bg_color.rgba = (0, 0, 0, 1)  # black when not selected

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.selected = data.get('selected', False)
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.select_task(self.index)
            return True
        return False

class ToDoApp(App):
    def build(self):
        self.tasks = []  # List of tasks, each as dict: {'task': str, 'due': int, 'diff': int, 'prio': float}
        self.selected_index = None
        self.root = Builder.load_string(KV)
        return self.root

    def add_task(self, task_text, due_text, diff_text):
        if not task_text or not due_text or not diff_text:
            return
        try:
            due = int(due_text)
            diff = int(diff_text)
        except ValueError:
            return
        if due < 0 or diff < 1 or diff > 5:
            return
        # Calculate priority: diff/due if due > 0, else diff
        prio = diff / due if due > 0 else diff
        self.tasks.append({'task': task_text, 'due': due, 'diff': diff, 'prio': prio})
        self.update_rv()

    def update_rv(self):
        """Refresh the RecycleView data and update selection status."""
        rv_data = []
        for idx, task in enumerate(self.tasks):
            rv_data.append({
                'text': f"{task['task']} | Due: {task['due']} | Diff: {task['diff']} | Prio: {task['prio']:.2f}",
                'index': idx,
                'selected': (self.selected_index == idx)
            })
        self.root.ids.rv.data = rv_data

    def select_task(self, index):
        """Select or deselect a task."""
        if self.selected_index == index:
            self.selected_index = None
        else:
            self.selected_index = index
        self.update_rv()

    def remove_task(self):
        """Remove the currently selected task."""
        if self.selected_index is None:
            return
        if 0 <= self.selected_index < len(self.tasks):
            self.tasks.pop(self.selected_index)
        self.selected_index = None
        self.update_rv()

    def sort_tasks(self):
        """Sort tasks by descending priority."""
        self.tasks.sort(key=lambda t: t['prio'], reverse=True)
        self.selected_index = None
        self.update_rv()

    def schedule_midnight_update(self):
        """Schedule update_due_dates to run at the next midnight."""
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        midnight = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
        seconds_until_midnight = (midnight - now).total_seconds()
        Clock.schedule_once(self.update_due_dates, seconds_until_midnight)
        print(f"Scheduled update in {seconds_until_midnight:.0f} seconds.")

    def update_due_dates(self, dt):
        """
        For each task, decrease due date by 1 (if above 0) and recalc priority.
        Priority is diff/due if due > 0, else diff.
        """
        for task in self.tasks:
            if task['due'] > 0:
                task['due'] -= 1
            task['prio'] = task['diff'] / task['due'] if task['due'] > 0 else task['diff']
        self.update_rv()
        self.schedule_midnight_update()

    def on_start(self):
        # Schedule the midnight update when the app starts.
        self.schedule_midnight_update()

if __name__ == '__main__':
    ToDoApp().run()
