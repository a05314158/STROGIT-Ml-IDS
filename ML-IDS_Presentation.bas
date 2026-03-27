Sub CreateMLIDSPresentation()
    Dim pptApp As Object
    Dim prs As Object
    Dim slide As Object
    Dim shape As Object
    Dim tf As Object
    
    Set pptApp = CreateObject("PowerPoint.Application")
    pptApp.Visible = True
    
    Set prs = pptApp.Presentations.Add()
    
    ' Slide 1: Title
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 2000000, 9000000, 1500000)
    Set tf = shape.TextFrame
    tf.Text = "ML-IDS Genesis v3.8"
    With tf.Paragraphs(1)
        .Font.Size = 60
        .Font.Bold = True
        .Font.Color.RGB = RGB(255, 255, 255)
        .Alignment = 2
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 4200000, 9000000, 1000000)
    Set tf = shape.TextFrame
    tf.Text = "Система обнаружения вторжений"
    With tf.Paragraphs(1)
        .Font.Size = 32
        .Font.Color.RGB = RGB(255, 255, 255)
        .Alignment = 2
    End With
    
    ' Slide 2: Problem
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Проблема"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "• Традиционные IDS основаны на сигнатурах" & vbCrLf & _
              "• Не обнаруживают zero-day уязвимости" & vbCrLf & _
              "• Высокий процент false positives (5-10%)" & vbCrLf & _
              "• Требуют постоянного обновления" & vbCrLf & _
              "• Не масштабируются на 1000+ устройств"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 3: Architecture
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Архитектура"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "Сенсор: Захват пакетов → 13 признаков" & vbCrLf & _
              "Веб-сервер: REST API + Pydantic" & vbCrLf & _
              "ML Worker: TensorFlow + Celery" & vbCrLf & _
              "База данных: PostgreSQL + Redis" & vbCrLf & _
              "Безопасность: Multi-tenant"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 4: Deep Autoencoder
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Deep Autoencoder"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "Архитектура: 13 → 8 → 13" & vbCrLf & _
              "Входной слой: 13 признаков трафика" & vbCrLf & _
              "Скрытый слой: 8 нейронов" & vbCrLf & _
              "Выходной слой: восстановление" & vbCrLf & _
              "Обнаружение: Если L(x) > 0.85 → Аномалия"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 5: Features
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "13 ключевых признаков"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "• Энтропия портов, Количество пакетов" & vbCrLf & _
              "• Средний размер, Стд. отклонение" & vbCrLf & _
              "• SYN/ACK отношение, Дисперсия интервалов" & vbCrLf & _
              "• Уникальные IP, Энтропия IP" & vbCrLf & _
              "• Количество доменов, TCP/UDP, DNS, Задержка"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 6: Performance
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Оптимизация производительности"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "До: 1100+ SQL запросов, 2-3 сек, 10 req/sec" & vbCrLf & _
              "После: 2-3 SQL запроса, 50ms, 500+ req/sec" & vbCrLf & vbCrLf & _
              "Техники: Bulk UPSERT, Model Caching, 4 Workers" & vbCrLf & _
              "Результат: 550x улучшение!"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 7: Metrics
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Ключевые метрики"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "• Throughput: 500+ запросов в секунду" & vbCrLf & _
              "• Latency: 50 миллисекунд" & vbCrLf & _
              "• ML Prediction: 5 миллисекунд" & vbCrLf & _
              "• Точность: 94-97%" & vbCrLf & _
              "• False Positive Rate: 2-3%"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 8: Security
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Безопасность"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "• API-аутентификация для каждого сенсора" & vbCrLf & _
              "• Pydantic валидация всех входных данных" & vbCrLf & _
              "• Multi-tenant архитектура с полной изоляцией" & vbCrLf & _
              "• Шифрование API-ключей в БД" & vbCrLf & _
              "• Аудит-логи всех действий"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 9: Threats
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Обнаруживаемые угрозы"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "• DDoS-атаки" & vbCrLf & _
              "• Сканирование портов" & vbCrLf & _
              "• Вредоносный трафик" & vbCrLf & _
              "• Утечки данных" & vbCrLf & _
              "• Несанкционированный доступ"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 10: Results
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Результаты"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "Точность: 94-97%" & vbCrLf & _
              "False Positive Rate: 2-3%" & vbCrLf & _
              "Время обнаружения: 5-50ms" & vbCrLf & _
              "Обнаруживает zero-day атаки" & vbCrLf & _
              "Самообучается каждые 24 часа"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 11: Use Cases
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Применение"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "Корпоративная сеть: Мониторинг трафика" & vbCrLf & _
              "ISP: Обнаружение ботнетов, защита от DDoS" & vbCrLf & _
              "Критическая инфраструктура: SCADA, промышленные сети" & vbCrLf & _
              "Соответствие регуляциям: GDPR, HIPAA, PCI-DSS"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 12: Conclusions
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(245, 247, 250)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 400000, 9000000, 800000)
    Set tf = shape.TextFrame
    tf.Text = "Выводы"
    With tf.Paragraphs(1)
        .Font.Size = 44
        .Font.Bold = True
        .Font.Color.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(1000000, 1800000, 8000000, 5500000)
    Set tf = shape.TextFrame
    tf.WordWrap = True
    tf.Text = "Deep Learning превосходит сигнатурные методы" & vbCrLf & _
              "Autoencoder обнаруживает неизвестные атаки" & vbCrLf & _
              "Оптимизация критична (550x улучшение)" & vbCrLf & _
              "Multi-tenant архитектура обеспечивает безопасность" & vbCrLf & _
              "Production-ready для 1000+ устройств"
    With tf.Paragraphs(1)
        .Font.Size = 20
        .Font.Color.RGB = RGB(45, 55, 72)
    End With
    
    ' Slide 13: Thank You
    Set slide = prs.Slides.Add(prs.Slides.Count + 1, 6)
    With slide.Background.Fill
        .Solid
        .ForeColor.RGB = RGB(102, 126, 234)
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 2000000, 9000000, 1500000)
    Set tf = shape.TextFrame
    tf.Text = "Спасибо за внимание!"
    With tf.Paragraphs(1)
        .Font.Size = 60
        .Font.Bold = True
        .Font.Color.RGB = RGB(255, 255, 255)
        .Alignment = 2
    End With
    
    Set shape = slide.Shapes.AddTextBox(500000, 4200000, 9000000, 1000000)
    Set tf = shape.TextFrame
    tf.Text = "Вопросы и обсуждение"
    With tf.Paragraphs(1)
        .Font.Size = 32
        .Font.Color.RGB = RGB(255, 255, 255)
        .Alignment = 2
    End With
    
    ' Save presentation
    prs.SaveAs CreateObject("WScript.Shell").SpecialFolders("Desktop") & "\ML-IDS_Conference\ML-IDS_Conference.pptx"
    
    MsgBox "Презентация создана успешно!" & vbCrLf & "Слайдов: " & prs.Slides.Count, vbInformation, "ML-IDS Genesis v3.8"
    
End Sub
