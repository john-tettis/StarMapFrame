<!DOCTYPE html>
<html lang="fa-ir" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="//fdn.fontcdn.ir">
    <link rel="preconnect" href="//v1.fontapi.ir">
    <link href="https://v1.fontapi.ir/css/Sahel" rel="stylesheet">
    <title>Invoice</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Sahel', sans-serif;
        }

        p {
            margin-bottom: 5px;
        }

        div.container {
            max-width: 700px;
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
            width: 100%;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            flex-flow: column;
            padding-bottom: 10px;
        }

        div.info>div {
            white-space: nowrap;
        }

        div.info>div>p {
            font-weight: bold;
            margin-left: 40px;
        }

        div.info>div>p>span {
            font-weight: normal;
            white-space: normal;
        }

        div.sender {
            margin-right: 25px;
            margin-bottom: 0px;
            padding: 5px 10px;
            border-right: 1px solid gray;
            font-size: 14px;
        }

        div.customer {
            margin-top: 0px;
            margin-right: 25px;
            margin-bottom: 0px;
            padding: 5px 10px;
            border-right: 1px solid gray;
            font-size: 14px;
        }
        div.customer > p{
            display: block;
        }
    </style>
</head>

<body>
    <?php if (@$_REQUEST['items'] == NULL) : ?>
        <div class="container">
            <div class="header">
                <div>
                    <img src="https://sky.respina.store/api/starmap/assets/logo.png" alt="logo" width="100" />
                </div>
                <div>
                    <h1>???????????? ??????????</h1>
                    <h6>???? ????????????: <?php echo $_REQUEST['tracking'] ?></h6>
                </div>
            </div>
            <div class="info">
                <div class="sender">
                    <p style="font-size:16px">??????????????: ???????????? ?????????? - ???????? ?????????????? (<span>??????????????????????</span>)</p>
                </div>
                <div class="customer">
                    <p style="font-size:16px">????????????: <?php echo $_REQUEST['name'] ?> (<span><?php echo $_REQUEST['mobile'] ?></span>)</p>
                    <p>???????? ????????: <span><?php echo $_REQUEST['province'] ?> - <?php echo $_REQUEST['city'] ?> - <?php echo $_REQUEST['address'] ?></span></p>
                    <p>???? ????????: <span><?php echo $_REQUEST['post'] ?></span></p>
                </div>
            </div>
        </div>
    <?php else : ?>
        <?php
        $object = urldecode(stripslashes($_REQUEST['items']));
        $items = json_decode($object, true);
        foreach ($items as $val) { ?>
            <div class="container" style="margin-bottom: 10px;">
                <div class="header">
                    <div>
                        <img src="https://sky.respina.store/api/starmap/assets/logo.png" alt="logo" width="100" />
                    </div>
                    <div>
                        <h1>???????????? ??????????</h1>
                        <h6>???? ????????????: <?php echo $val['tracking'] ?></h6>
                    </div>
                </div>
                <div class="info">
                    <div class="sender">
                        <p style="font-size:16px">??????????????: ???????????? ?????????? - ???????? ?????????????? (<span>??????????????????????</span>)</p>
                    </div>
                    <div class="customer">
                        <p style="font-size:16px">????????????: <?php echo $val['name'] ?> (<span><?php echo $val['mobile'] ?></span>)</p>
                        <p>???????? ????????: <span><?php echo $val['province'] ?> - <?php echo $val['city'] ?> - <?php echo $val['address'] ?></span></p>
                        <p>???? ????????: <span><?php echo $val['post'] ?></span></p>
                    </div>
                </div>
            </div>
    <?php }
    endif; ?>
</body>

</html>