# The proper term is pseudo_replica_mode, but we use this compatibility alias
# to make the statement usable on server versions 8.0.24 and older.
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
# at 4
#241112 16:21:16 server id 1  end_log_pos 126 CRC32 0xab8c89d1 	Start: binlog v 4, server v 8.0.40 created 241112 16:21:16 at startup
ROLLBACK/*!*/;
BINLOG '
bHIzZw8BAAAAegAAAH4AAAAAAAQAOC4wLjQwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAABscjNnEwANAAgAAAAABAAEAAAAYgAEGggAAAAICAgCAAAACgoKKioAEjQA
CigAAdGJjKs=
'/*!*/;
# at 126
#241112 16:21:16 server id 1  end_log_pos 157 CRC32 0x68e83ade 	Previous-GTIDs
# [empty]
# at 157
#241112 23:24:48 server id 1  end_log_pos 236 CRC32 0xe1ee61f6 	Anonymous_GTID	last_committed=0	sequence_number=1	rbr_only=no	original_committed_timestamp=1731450288916635	immediate_commit_timestamp=1731450288916635	transaction_length=257
# original_commit_timestamp=1731450288916635 (2024-11-12 23:24:48.916635 Maroc (heure d’été))
# immediate_commit_timestamp=1731450288916635 (2024-11-12 23:24:48.916635 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731450288916635*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 236
#241112 23:24:48 server id 1  end_log_pos 414 CRC32 0xe3dac0ef 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 386
use `elearning_platform`/*!*/;
SET TIMESTAMP=1731450288/*!*/;
SET @@session.pseudo_thread_id=44/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=1168113696/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C cp850 *//*!*/;
SET @@session.character_set_client=4,@@session.collation_connection=4,@@session.collation_server=255/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
/*!80011 SET @@session.default_collation_for_utf8mb4=255*//*!*/;
CREATE INDEX idx_courses_title_status ON courses (title, status)
/*!*/;
# at 414
#241113  0:14:26 server id 1  end_log_pos 491 CRC32 0x689c0597 	Anonymous_GTID	last_committed=1	sequence_number=2	rbr_only=no	original_committed_timestamp=1731453266639989	immediate_commit_timestamp=1731453266639989	transaction_length=249
# original_commit_timestamp=1731453266639989 (2024-11-13 00:14:26.639989 Maroc (heure d’été))
# immediate_commit_timestamp=1731453266639989 (2024-11-13 00:14:26.639989 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731453266639989*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 491
#241113  0:14:26 server id 1  end_log_pos 663 CRC32 0xb9026d10 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 546
SET TIMESTAMP=1731453266/*!*/;
CREATE INDEX idx_users_id_role_student ON users (id, role)
/*!*/;
# at 663
#241113  0:15:36 server id 1  end_log_pos 742 CRC32 0xcf1357c6 	Anonymous_GTID	last_committed=2	sequence_number=3	rbr_only=no	original_committed_timestamp=1731453336180073	immediate_commit_timestamp=1731453336180073	transaction_length=297
# original_commit_timestamp=1731453336180073 (2024-11-13 00:15:36.180073 Maroc (heure d’été))
# immediate_commit_timestamp=1731453336180073 (2024-11-13 00:15:36.180073 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731453336180073*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 742
#241113  0:15:36 server id 1  end_log_pos 960 CRC32 0x20b80616 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 547
SET TIMESTAMP=1731453336/*!*/;
CREATE INDEX idx_enrollments_student_course_date ON enrollments (student_id, course_id, enrollment_date)
/*!*/;
# at 960
#241113  0:16:04 server id 1  end_log_pos 1037 CRC32 0xdb7f4520 	Anonymous_GTID	last_committed=3	sequence_number=4	rbr_only=no	original_committed_timestamp=1731453364924016	immediate_commit_timestamp=1731453364924016	transaction_length=247
# original_commit_timestamp=1731453364924016 (2024-11-13 00:16:04.924016 Maroc (heure d’été))
# immediate_commit_timestamp=1731453364924016 (2024-11-13 00:16:04.924016 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731453364924016*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 1037
#241113  0:16:04 server id 1  end_log_pos 1207 CRC32 0x87d7fadf 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 548
SET TIMESTAMP=1731453364/*!*/;
CREATE INDEX idx_users_email_role ON users (email, role)
/*!*/;
# at 1207
#241113  0:25:32 server id 1  end_log_pos 1286 CRC32 0x03b012c2 	Anonymous_GTID	last_committed=4	sequence_number=5	rbr_only=no	original_committed_timestamp=1731453932481811	immediate_commit_timestamp=1731453932481811	transaction_length=503
# original_commit_timestamp=1731453932481811 (2024-11-13 00:25:32.481811 Maroc (heure d’été))
# immediate_commit_timestamp=1731453932481811 (2024-11-13 00:25:32.481811 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731453932481811*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 1286
#241113  0:25:32 server id 1  end_log_pos 1710 CRC32 0x1af80a3b 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 550
SET TIMESTAMP=1731453932.467248/*!*/;
CREATE DEFINER=`root`@`localhost` TRIGGER before_price_update
BEFORE UPDATE ON courses
FOR EACH ROW
BEGIN
    IF OLD.price <> NEW.price THEN
        INSERT INTO price_history (course_id, old_price, new_price, changed_at)
        VALUES (OLD.id, OLD.price, NEW.price, NOW());
    END IF;
END
/*!*/;
# at 1710
#241113  0:46:24 server id 1  end_log_pos 1789 CRC32 0x15fa1d22 	Anonymous_GTID	last_committed=5	sequence_number=6	rbr_only=no	original_committed_timestamp=1731455184845540	immediate_commit_timestamp=1731455184845540	transaction_length=854
# original_commit_timestamp=1731455184845540 (2024-11-13 00:46:24.845540 Maroc (heure d’été))
# immediate_commit_timestamp=1731455184845540 (2024-11-13 00:46:24.845540 Maroc (heure d’été))
/*!80001 SET @@session.original_commit_timestamp=1731455184845540*//*!*/;
/*!80014 SET @@session.original_server_version=80040*//*!*/;
/*!80014 SET @@session.immediate_server_version=80040*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 1789
#241113  0:46:24 server id 1  end_log_pos 2564 CRC32 0x51db7b25 	Query	thread_id=44	exec_time=0	error_code=0	Xid = 567
SET TIMESTAMP=1731455184.828799/*!*/;
CREATE DEFINER=`root`@`localhost` TRIGGER after_status_update
AFTER UPDATE ON progress_tracking
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND OLD.status <> 'completed' THEN
        
        UPDATE progress_tracking
        SET completion_date = NOW()
        WHERE id = NEW.id;
        
    ELSEIF NEW.status = 'in_progress' AND OLD.status <> 'in_progress' THEN
        
        UPDATE progress_tracking
        SET start_date = NOW()
        WHERE id = NEW.id;
        
    ELSEIF NEW.status <> 'completed' THEN
        
        UPDATE progress_tracking
        SET completion_date = NULL
        WHERE id = NEW.id;
    END IF;
END
/*!*/;
# at 2564
#241114  0:20:28 server id 1  end_log_pos 2587 CRC32 0x140f6ea6 	Stop
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
