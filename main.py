import flet as ft

# لیست گره‌ها
nodes_graph = []

def main(page: ft.Page):
    # تنظیمات صفحه
    page.title = "Do Visualization"
    page.padding = 0
    page.adaptive = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    def on_resize(e):
        # look a like page.update() dosent work,soo...
        #this is for fixing the search container width
        parent = 0
        child = 0
        if len(page.overlay) > 0:
            for i in page.overlay:
                if isinstance(i, ft.Stack) and i.controls:
                    for control in i.controls:
                        if isinstance(control, ft.Column):
                            page.overlay[0].controls[0].width = page.width
                            page.update(page.overlay[0].controls[0])
                            child+=1
                parent+=1
        #--------------------------------------------------------------------



        page.update()
    page.on_resized = on_resize



        
    # تابع برای به‌روزرسانی ابعاد و تنظیمات circle_holder
    def update_circle_holder():
        if not nodes_graph:
            return
        # پیدا کردن کمترین و بیشترین left و top
        max_left = max(node.left + node.content.width for node in nodes_graph)
        max_top = max(node.top + node.content.height for node in nodes_graph)
        min_left = min(node.left for node in nodes_graph)
        min_top = min(node.top for node in nodes_graph)
        
        # تنظیم ابعاد circle_holder با حاشیه 100 پیکسلی
        margin = 100
        circle_holder.width = max(3000, max_left - min_left + 2 * margin)
        circle_holder.height = max(3000, max_top - min_top + 2 * margin)
        
        # تنظیم موقعیت گره‌ها نسبت به min_left و min_top
        for node in nodes_graph:
            node.left -= min_left - margin
            node.top -= min_top - margin
        
        # تنظیم boundary_margin
        viewer.boundary_margin = ft.Margin(
            circle_holder.width / 2,
            circle_holder.height / 2,
            circle_holder.width / 2,
            circle_holder.height / 2,
        )
        
        # تنظیم min_scale
        viewer.min_scale = min(
            page.width / circle_holder.width,
            page.height / circle_holder.height,
            0.01,  # حداقل مقیاس
        )
        page.update()

    # تابع‌های مربوط به گره‌ها (مانند جابه‌جایی و کلیک)
    def circle_on_click(e):
        global selected_node
        if selected_node:
            selected_node.border = None
            page.update(selected_node)
        selected_node = e.control
        e.control.border = ft.border.all(10, ft.Colors.BLUE_ACCENT_400)
        page.update(e.control)

    def on_pan_start(e: ft.DragUpdateEvent):
        e.control.content.shadow = None
        e.control.content.update()

    def on_pan_end(e: ft.DragUpdateEvent):
        e.control.content.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK)
        update_circle_holder()  # به‌روزرسانی بعد از جابه‌جایی
        e.control.content.update()

    def on_pan_update(e: ft.DragUpdateEvent):
        e.control.top = e.control.top + e.delta_y
        e.control.left = e.control.left + e.delta_x
        e.control.update()

    # ایجاد گره‌های اولیه
    circle = ft.Container(
        content=ft.Text("circle1"),
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.GREEN,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK),
        on_click=circle_on_click,
        alignment=ft.alignment.center,
        width=100,
        height=100,
    )
    circle2 = ft.Container(
        content=ft.Text("circle2"),
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.RED,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK),
        on_click=circle_on_click,
        alignment=ft.alignment.center,
        width=100,
        height=100,
    )
    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        drag_interval=10,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        on_pan_start=on_pan_start,
        content=circle,
        left=page.width / 2,
        top=page.height / 2,
    )
    gd2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.CLICK,
        drag_interval=10,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        on_pan_start=on_pan_start,
        content=circle2,
        left=100,
        top=100,
    )
    nodes_graph.append(gd)
    nodes_graph.append(gd2)

    # ایجاد circle_holder و InteractiveViewer
    circle_holder = ft.Stack(
        [gd, gd2],
        width=3000,  # ابعاد اولیه
        height=3000,
        clip_behavior=ft.ClipBehavior.NONE,
    )

    viewer = ft.InteractiveViewer(
        content=circle_holder,
        width=page.width,
        height=page.height,
        clip_behavior=ft.ClipBehavior.NONE,
        pan_enabled=True,
        scale_enabled=True,
        min_scale=0.01,
        max_scale=10.0,
        boundary_margin=ft.Margin(1000, 1000, 1000, 1000),
    )
    page.add(viewer)

    # تابع برای اضافه کردن گره جدید
    def add_node(e):
        new_circle = ft.Container(
            content=ft.Text(f"circle{len(nodes_graph) + 1}"),
            shape=ft.BoxShape.CIRCLE,
            bgcolor=ft.Colors.BLUE,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK),
            on_click=circle_on_click,
            alignment=ft.alignment.center,
            width=100,
            height=100,
        )
        new_gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            drag_interval=10,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end,
            on_pan_start=on_pan_start,
            content=new_circle,
            left=200,
            top=200,
        )
        nodes_graph.append(new_gd)
        circle_holder.controls.append(new_gd)
        update_circle_holder()  # به‌روزرسانی بعد از اضافه کردن گره
        page.update()






    # search ------------------------------------------------------------------------------------------------------------------------
    def close_anchor(e):
        if e.control.data:
            text = f"Color {e.control.data}"
            print(f"closing view from {text}")
            search_container.close_view(text)
        else:
            search_container.close_view()

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        search_container.open_view()
    
    def close_search(e):
        page.overlay.remove(search_container_holder)
        page.update()

    def amenity_selected(e):
        page.update()
    def open_filter(e):
        search_container_holder.controls[0].controls.append(
            ft.Row(
                controls=[
                    ft.Chip(
                        label=ft.Text('Search By Title'),
                        # bgcolor=ft.Colors.GREEN_200,
                        disabled_color=ft.Colors.GREEN_100,
                        autofocus=True,
                        on_select=amenity_selected,
                    ),
                    ft.Chip(
                        label=ft.Text('Search By Contents'),
                        # bgcolor=ft.Colors.GREEN_200,
                        disabled_color=ft.Colors.GREEN_100,
                        autofocus=True,
                        on_select=amenity_selected,
                    ),
                    ft.Chip(
                        label=ft.Text('Search By Contents Files'),
                        # bgcolor=ft.Colors.GREEN_200,
                        disabled_color=ft.Colors.GREEN_100,
                        autofocus=True,
                        on_select=amenity_selected,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            
        )
        search_container.view_trailing = [ft.IconButton(icon=ft.Icons.FILTER_ALT, on_click=open_filter)]
        search_container.view_trailing[0].on_click = close_filter
        close_anchor(e)
        page.update()

    def close_filter(e):
        search_container.view_trailing = [ft.IconButton(icon=ft.Icons.FILTER_ALT_OFF_OUTLINED, on_click=open_filter)]
        search_container.view_trailing[0].on_click = open_filter
        close_anchor(e)
        search_container_holder.controls[0].controls.remove(search_container_holder.controls[0].controls[2])

        page.update()

    search_container = ft.SearchBar(
        # view_elevation=2,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search nodes...",
        view_hint_text="for better results change the filter -->",
        bar_leading = ft.IconButton(icon=ft.Icons.CLOSE, on_click=close_search),
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        view_trailing = [ft.IconButton(icon=ft.Icons.FILTER_ALT_OFF_OUTLINED, on_click=open_filter)],
        controls=[
            ft.ListTile(
            
            )
        ],
        width=page.width,
    )
    # to set the padding of the search container
    search_container_holder=ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("\n"),
                    ft.Container(
                        width=page.width,
                        content=search_container,
                        alignment=ft.alignment.center,
                        padding=10,
                        
                    ),


                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        
            ft.Container(
                content=ft.FloatingActionButton(
                icon=ft.Icons.ARROW_FORWARD,
                bgcolor=ft.Colors.BLUE,
                shape=ft.CircleBorder(),
                on_click=lambda e: print("FAB 1 کلیک شد")
            ),
            right=20, bottom=20),
            ft.Container(
                content=ft.FloatingActionButton(
                icon=ft.Icons.ARROW_BACK,
                bgcolor=ft.Colors.BLUE,
                shape=ft.CircleBorder(),
                on_click=lambda e: print("FAB 2 کلیک شد"),
            ),
            left=20, bottom=20)
            
            
        ],
        width=page.width,
        height=page.height,
        )
     
    # ----------------------------------------------------------------------------------------------------------------------------------------












    # chat ------------------------------------------------------------------------------------------------------------------------
    chat_with_agent =ft.BottomSheet(
        enable_drag=True,
        is_scroll_controlled=True,
        maintain_bottom_view_insets_padding=True,
        show_drag_handle=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,

                controls=[
                    ft.Text("This is bottom sheet's content!"),
                    ft.ElevatedButton("Close bottom sheet", on_click=lambda _: page.close(chat_with_agent)),
                ],
            ),
        ),
    )
    # ----------------------------------------------------------------------------------------------------------------------------------------











    # buttom app bar ------------------------------------------------------------------------------------------------------------------------
    def chat_button_click(e):
        page.open(chat_with_agent)
        page.update()
    chat_button = ft.FloatingActionButton(icon=ft.Icons.CHAT, on_click=chat_button_click,shape=ft.CircleBorder())
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
    # تنظیمات BottomAppBar و دکمه اضافه کردن گره
    def on_plus_click(e):
        add_node(e)  # مثلاً برای تست، گره جدید اضافه کن
    def remove_node(e):
        page.update()
    def edit_node(e):
        page.update()
    def search_node(e):
        page.overlay.append(search_container_holder)
        page.update()
    bottom_app_bar = ft.BottomAppBar(
        content=ft.Row(
            [
                ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_node),
                ft.IconButton(icon=ft.Icons.REMOVE, on_click=remove_node),
                ft.IconButton(icon=ft.Icons.ADD, on_click=on_plus_click),
                ft.IconButton(icon=ft.Icons.SEARCH, on_click=search_node),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=ft.Colors.BLUE_100,
        shape=ft.NotchShape.CIRCULAR,
    )
    page.add(bottom_app_bar,chat_button)
    # ----------------------------------------------------------------------------------------------------------------------------------------

ft.app(target=main)
