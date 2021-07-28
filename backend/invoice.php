<!DOCTYPE html>
<html lang="fa-ir" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice</title>
    <style>
        @font-face {
            font-family: "IranSans";
            src: url("/fonts/IRANSansXFaNum-Regular.woff") format('woff'),
            url("/fonts/IRANSansXFaNum-Regular.woff2") format('woff2');
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'IranSans', sans-serif;
        }

        p {
            margin-bottom: 5px;
        }

        div.container {
            max-width: 900px;
            background-color: aliceblue;
            border-radius: 0px;
        }

        div.header {
            display: flex;
            flex-flow: row wrap;
            align-items: center;
            justify-content: flex-start;

        }
        
        div.info {
            min-height: 300px;
            width: 100%;
            display:flex;
            align-items:flex-start;
            justify-content: center;
            flex-flow: column
        }

        div.info>div {
            white-space: nowrap;
        }
        div.info>div>p{
            font-weight: bold
        }
        div.info>div>p>span{
            font-weight: normal;
        }
        div.sender{
            margin-right: 25px;
            margin-bottom: 10px;
            padding: 10px 10px;
            border-right: 1px solid gray;
            font-size: 14px;
        }
        div.customer{
            margin-top: 10px;
            margin-right: 25px;
            margin-bottom: 5px;
            padding: 10px 10px;
            border-right: 1px solid gray;
            font-size: 14px;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div>
                <img src="http://localhost:5000/download/logo.png" alt="logo" width="100" />
            </div>
            <div>
                <h1>رسپینا گالری</h1>
                <h6>کد پیگیری: <?php echo $_REQUEST['tracking'] ?></h6>
            </div>
        </div>
        <div class="info">
                <div class="sender">
                    <p style="font-size:16px">فرستنده: رسپینا گالری - الهه میرزایی</p>
                    <p>شماره تماس: <span>۰۹۱۰۳۸۰۷۳۳۱</span></p>
                    <p>کد پستی: <span>۱۸۴۳۷۱۳۳۷۵</span></p>
                    <p>آدرس: <span>تهران - میدان شهدای شاملو - خیابان مدرسه - خیابان ورزشگاه - رسپینا</span></p>
                </div>
                <div class="customer">
                    <p style="font-size:16px">گیرنده: <?php echo $_REQUEST['name'] ?></p>
                    <p>شماره تماس: <span><?php echo $_REQUEST['mobile'] ?></span></p>
                    <p>آدرس کامل: <span><?php echo $_REQUEST['province'] ?> - <?php echo $_REQUEST['city'] ?> - <?php echo $_REQUEST['address'] ?></span></p>
                    <p>کد پستی: <span><?php echo $_REQUEST['post'] ?></span></p>
                </div>
        </div>
    </div>
</body>

</html>